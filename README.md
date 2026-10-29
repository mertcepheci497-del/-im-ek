# ⚡ ŞİMŞEK Moderasyon Botu

## Kurulum
1. `pip install -r requirements.txt`
2. `DISCORD_TOKEN` ortam değişkenini ayarlayın.
3. Developer Portal'da **Message Content** ve **Server Members** intent'lerini açın.
4. `python main.py`

## Yapı
- `main.py` — Bot başlatma, hata yönetimi, loglama
- `config.py` — Tüm ayarlar (filtreler, süreler, renkler)
- `database.py` — Asenkron SQLite (`simsek_moderasyon.db`)
- `cogs/` — Modüller: automod, moderation, warnings, logs, settings, tickets, info, forum
