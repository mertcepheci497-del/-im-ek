"""Asenkron SQLite katmanı."""

import datetime

import aiosqlite

SETTING_KEYS = {
    "log_channel_id",
    "welcome_channel_id",
    "autorole_id",
    "ticket_category_id",
    "ticket_staff_role_id",
    "forum_channel_id",
}


class Database:
    def __init__(self, path: str):
        self.path = path
        self.conn: aiosqlite.Connection | None = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
                guild_id INTEGER PRIMARY KEY,
                log_channel_id INTEGER
            )
        """)
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                user_id INTEGER,
                reason TEXT,
                moderator_id INTEGER,
                timestamp TEXT
            )
        """)
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_config (
                key TEXT PRIMARY KEY,
                value INTEGER
            )
        """)
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS guild_threads (
                guild_id INTEGER PRIMARY KEY,
                thread_id INTEGER,
                name TEXT,
                invite TEXT
            )
        """)
        for col in SETTING_KEYS - {"log_channel_id"}:
            try:
                await self.conn.execute(
                    f"ALTER TABLE guild_settings ADD COLUMN {col} INTEGER"
                )
            except aiosqlite.OperationalError:
                pass
        await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def get_settings(self, guild_id: int) -> dict:
        async with self.conn.execute(
            "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
        ) as cur:
            row = await cur.fetchone()
        return dict(row) if row else {}

    async def set_setting(self, guild_id: int, key: str, value):
        if key not in SETTING_KEYS:
            raise ValueError(f"Geçersiz ayar: {key}")
        await self.conn.execute(
            "INSERT OR IGNORE INTO guild_settings (guild_id) VALUES (?)",
            (guild_id,),
        )
        await self.conn.execute(
            f"UPDATE guild_settings SET {key} = ? WHERE guild_id = ?",
            (value, guild_id),
        )
        await self.conn.commit()

    async def get_global(self, key: str):
        async with self.conn.execute(
            "SELECT value FROM bot_config WHERE key = ?", (key,)
        ) as cur:
            row = await cur.fetchone()
        return row[0] if row else None

    async def set_global(self, key: str, value):
        await self.conn.execute(
            "INSERT OR REPLACE INTO bot_config (key, value) VALUES (?, ?)", (key, value)
        )
        await self.conn.commit()

    async def get_guild_thread(self, guild_id: int):
        async with self.conn.execute(
            "SELECT * FROM guild_threads WHERE guild_id = ?", (guild_id,)
        ) as cur:
            return await cur.fetchone()

    async def set_guild_thread(self, guild_id, thread_id, name, invite):
        await self.conn.execute(
            "INSERT OR REPLACE INTO guild_threads (guild_id, thread_id, name, invite)"
            " VALUES (?, ?, ?, ?)",
            (guild_id, thread_id, name, invite),
        )
        await self.conn.commit()

    async def list_guild_threads(self):
        async with self.conn.execute(
            "SELECT * FROM guild_threads ORDER BY name COLLATE NOCASE"
        ) as cur:
            return await cur.fetchall()

    async def delete_guild_thread_by_thread(self, thread_id):
        await self.conn.execute(
            "DELETE FROM guild_threads WHERE thread_id = ?", (thread_id,)
        )
        await self.conn.commit()

    async def add_warning(self, guild_id, user_id, reason, moderator_id) -> int:
        await self.conn.execute(
            "INSERT INTO warnings (guild_id, user_id, reason, moderator_id, timestamp)"
            " VALUES (?, ?, ?, ?, ?)",
            (guild_id, user_id, reason, moderator_id, str(datetime.datetime.now())),
        )
        await self.conn.commit()
        return await self.count_warnings(guild_id, user_id)

    async def count_warnings(self, guild_id, user_id) -> int:
        async with self.conn.execute(
            "SELECT COUNT(*) FROM warnings WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        ) as cur:
            return (await cur.fetchone())[0]

    async def get_warnings(self, guild_id, user_id, limit=20):
        async with self.conn.execute(
            "SELECT id, reason, moderator_id, timestamp FROM warnings"
            " WHERE guild_id = ? AND user_id = ? ORDER BY id DESC LIMIT ?",
            (guild_id, user_id, limit),
        ) as cur:
            return await cur.fetchall()

    async def delete_warning(self, guild_id, warning_id) -> bool:
        cur = await self.conn.execute(
            "DELETE FROM warnings WHERE id = ? AND guild_id = ?",
            (warning_id, guild_id),
        )
        await self.conn.commit()
        return cur.rowcount > 0

    async def clear_warnings(self, guild_id, user_id) -> int:
        cur = await self.conn.execute(
            "DELETE FROM warnings WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        await self.conn.commit()
        return cur.rowcount
