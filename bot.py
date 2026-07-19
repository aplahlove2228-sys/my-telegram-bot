import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956668860:AAH...")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

HAFEZ_POEMS = [
    {
        "title": "غزل شماره ۱",
        "poem": """اگر آن ترک شیرازی به دست آرد دل ما را
با سلسلهٔ زُلف، ما را از سر بندد به دلدار

با خِرامش چو قَدّسیان، نازپروردش چو پریشان
به فِدا دادن جان در طَلبِ کاروانسالار""",
        "meaning": "این غزل دربارهٔ عشق و دلدادگی است. حافظ از معشوق شیرازی سخن می‌گوید."
    },
    {
        "title": "غزل شماره ۲",
        "poem": """صبا به لطف بگو آن غَزّالِ رَعنا را
که سر به بادِ صبا دادی، بازمَده به ما را

شکایت از لبِ لعلِ تو، گر چه شیرین است لیکن
زِ عادت بد نپسندم، عَذرِ بدگوها را""",
        "meaning": "این غزل دربارهٔ دوری معشوق و انتظار بازگشت اوست."
    },
    {
        "title": "غزل شماره ۳",
        "poem": """ساقیا برخیز و دردِه جامِ را
خاک بر سرِ زهدِ فَراموش‌نامِ را

باده بده، شادی بده، غم مخور، راه بده
درده راحتِ دلِ غمدیدهٔ ایامِ را""",
        "meaning": "این غزل دربارهٔ زندگی و شادی است. حافظ از ساقی می‌خواهد باده بدهد."
    },
    {
        "title": "غزل شماره ۴",
        "poem": """دُرَختِ ایمانِ بِی‌بَرگ و بَر، عِشق است
وین رَهزَنِ عَقل و دین، عِشق است

هر آن کَس کِه بِه دامِ عِشق افتاد
از او نِشاط و شادی و سَرور است""",
        "meaning": "این غزل دربارهٔ قدرت عشق است. حافظ عشق را بالاتر از عقل می‌داند."
    },
    {
        "title": "غزل شماره ۵",
        "poem": """مَی خورَم و مَست و مَلولانَم
بِه دَورِ مَی و مَست و مَلولانَم

مَن آنِ مَستِ مَحوَم کِه دَر مَی
نَه نام و نَه نشان دارَم""",
        "meaning": "این غزل دربارهٔ حالت مستی و فنا در عشق است."
    }
]

FAL_TAABIR = {
    "خوب": [
        "🌟 فال شما خوب است! ایام خوشی در پیش دارید.",
        "✨ نیت شما مستجاب می‌شود. صبر کنید.",
        "🌙 موفقیت و سعادت در راه است.",
        "💫 خبر خوشی به زودی می‌شنوید.",
        "🌸 عشق و محبت در زندگی‌تان جاری می‌شود."
    ],
    "متوسط": [
        "⛅ فال شما متوسط است. با احتیاط پیش بروید.",
        "🌤️ نیت شما نیاز به تلاش بیشتر دارد.",
        "🍃 صبر و شکیبایی کلید موفقیت شماست.",
        "🌾 تغییراتی در راه است. آماده باشید.",
        "🌱 فرصت‌های خوبی پیش رو دارید."
    ],
    "سخت": [
        "🌧️ فال شما سخت است. مراقب باشید.",
        "⛈️ مشکلاتی در پیش است. قوی باشید.",
        "🌩️ نیت شما به زودی برآورده نمی‌شود. صبر کنید.",
        "🌪️ تغییراتی لازم است. خود را آماده کنید.",
        "❄️ سختی‌ها می‌گذرند. امید داشته باشید."
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌹 سلام به ربات فال حافظ خوش اومدی!\n\n"
        "📜 دستورات:\n"
        "/start - شروع\n"
        "/fal - گرفتن فال حافظ\n"
        "/help - راهنما\n\n"
        "✨ نیت کن و /fal بزن!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 راهنمای ربات فال حافظ:\n\n"
        "/fal - یه غزل تصادفی از حافظ + تعبیر فال\n\n"
        "✨ قبل از گرفتن فال، نیت کن و بعد دستور رو بزن."
    )

async def fal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poem = random.choice(HAFEZ_POEMS)
    taabir_type = random.choice(list(FAL_TAABIR.keys()))
    taabir = random.choice(FAL_TAABIR[taabir_type])
    
    message = (
        f"📜 {poem['title']}\n\n"
        f"{poem['poem']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"📝 معنی:\n{poem['meaning']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔮 تعبیر فال:\n{taabir}\n\n"
        f"✨ نیت کنید و صبر کنید..."
    )
    
    await update.message.reply_text(message)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("fal", fal))
    
    application.run_polling()

if __name__ == "__main__":
    main()
