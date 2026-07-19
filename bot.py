cd ~/mybot
cat > bot.py << 'EOF'
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956666860:AAHzvS0-eBvMAPpVNQsxIr80jKC8wdmxrtI")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام دوست من! 👋\n"
        "من ربات هوشمند هستم!\n\n"
        "دستورات من:\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/dice - تاس انداختن 🎲\n"
        "/coin - پرتاب سکه 🪙\n"
        "/joke - یه جوک 😂\n\n"
        "هر چی بگی برات تکرار میکنم! 😊"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 راهنما:\n\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/dice - تاس انداختن (۱ تا ۶)\n"
        "/coin - پرتاب سکه (شیر یا خط)\n"
        "/joke - یه جوک باحال\n\n"
        "هر پیامی بفرستی برات تکرار میکنم!"
    )

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 6)
    await update.message.reply_text(f"🎲 تاس انداختی: {number}")

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = random.choice(["شیر 🦁", "خط 🦅"])
    await update.message.reply_text(f"🪙 سکه پرتاب شد: {result}")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "چرا کامپیوتر به دکتر رفت؟ چون ویروس گرفته بود! 😂",
        "برنامه‌نویس وارد رستوران شد. گارسون پرسید: چی میل دارید؟ گفت: منوی اصلی رو نشون بده! 😅",
        "چرا جاوا اسکریپت به جاوا رفت؟ چون null بود! 🤣",
        "برنامه‌نویس‌ها چرا تاریکی رو دوست دارن؟ چون نور باعث باگ میشه! 💡",
    ]
    await update.message.reply_text(random.choice(jokes))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"تو گفتی: {update.message.text}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("coin", coin))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()

if __name__ == "__main__":
    main()
EOF
