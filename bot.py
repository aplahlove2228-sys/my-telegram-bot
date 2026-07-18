															import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# ⬇️ TOKEN از Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956666860:AAHzvS0-eBvMAPpVNQsxIr80jKC8wdmxrtI")

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app برای Keep Alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام دوست من! 👋\nربات آماده‌ست! چطور می‌تونم کمکت کنم؟")

# دستور /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستورات من:\n/start - شروع\n/help - راهنما")

# پاسخ به پیام‌های معمولی
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"تو گفتی: {update.message.text}")

def run_bot():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        logger.info("🤖 ربات در حال اجراست...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"خطا در ربات: {e}")

def main():
    # اجرای ربات در Thread جدا
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("ربات Thread شروع شد")
    
    # اجرای Flask
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Flask روی پورت {port} شروع میشه...")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()    
    # اجرای Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
