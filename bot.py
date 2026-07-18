import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# ⬇️ TOKEN از Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956666860:AAHzvS0-eBvMAPpVNQsxIr80jKC8wdmxrtI")

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# اجرای ربات
def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("🤖 ربات در حال اجراست...")
    application.run_polling()

def main():
    # اجرای ربات در Thread جدا
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # اجرای Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
