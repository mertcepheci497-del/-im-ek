"""ŞİMŞEK Bot — Merkezi ayarlar. Değiştirmek istediklerinizi buradan düzenleyin."""

import discord

DB_PATH = "simsek_moderasyon.db"

OWNER_IDS = ()

EXTENSIONS = (
    "cogs.automod",
    "cogs.moderation",
    "cogs.warnings",
    "cogs.logs",
    "cogs.settings",
    "cogs.tickets",
    "cogs.info",
    "cogs.forum",
)

RENK_ANA = discord.Color.gold()
RENK_BASARI = discord.Color.green()
RENK_HATA = discord.Color.red()
RENK_UYARI = discord.Color.orange()

SPAM_MESAJ_LIMITI = 4
SPAM_SURE = 3
CAPS_ORANI = 0.7
MAX_ETIKET = 5
IHLAL_LIMITI = 3
IHLAL_PENCERE = 600
IHLAL_TIMEOUT_DAKIKA = 10

YASAKLI_TAM = {"amk", "aq", "piç", "sik", "oç", "göt", "mk"}
YASAKLI_ONEK = ("orospu", "yarrak", "siktir", "amına", "amina", "ibne")

PHISHING = (
    "discord-nitro", "steam-gift", "free-nitro", "nitro-free",
    "airdrop", "steamcommunity.ru", "gift-nitro",
)
IZINLI_ALAN_ADLARI = ("tenor.com", "giphy.com", "youtube.com", "youtu.be")

OTOMATIK_TIMEOUT_UYARI = 3
OTOMATIK_TIMEOUT_DAKIKA = 60

KURALLAR_METNI = (
    "**1️⃣ Saygı:** Herkese saygılı davran. Hakaret, cadı avı, cinsiyet ayrımı,"
    " ırkçılık veya nefret söylemi yasaktır.\n"
    "**2️⃣ Reklam & Spam:** İzinsiz spam, sunucu daveti veya reklam (DM dahil)"
    " yasaktır.\n"
    "**3️⃣ NSFW:** Yaş sınırlı, +18 veya rahatsız edici içerik/bağlantı"
    " yasaktır.\n"
    "**4️⃣ Davranış:** Terörizm, flört, kavga, küfür ve zorbalık yasaktır.\n"
    "**5️⃣ Log Koruması:** Odalarda hızlı gezip logları kirletmek yasaktır.\n"
    "**6️⃣ Gizlilik:** Kimsenin kişisel verisini izinsiz paylaşmak yasaktır.\n"
    "**7️⃣ Etiket Spamı:** Yetkilileri/rolleri nedensiz etiketlemek yasaktır."
)
