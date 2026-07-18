import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ⬇️ TOKEN رباتت
BOT_TOKEN = "8956666860:AAHzvS0-eBvMAPpVNQsxIr80jKC8wdmxrtI"

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
def main():
    # ساخت اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # شروع ربات
    print("🤖 ربات در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
