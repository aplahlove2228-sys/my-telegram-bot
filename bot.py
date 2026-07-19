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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام دوست من! 👋\n"
        "به ربات من خوش اومدی!\n\n"
        "دستورات:\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/dice - تاس انداختن 🎲\n"
        "/coin - سکس پرتاب 🪙\n"
        "/joke - یه جوک 😂\n\n"
        "امیدوارم لذت ببری! 😊"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 راهنما:\n\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/dice - تاس انداختن (۱ تا ۶)\n"
        "/coin - سکس پرتاب (شیر یا خط)\n"
        "/joke - یه جوک\n\n"
        "امیدوارم لذت ببری!"
    )

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 6)
    await update.message.reply_text(f"🎲 تاس انداختن: {number}")

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = random.choice(["شیر 🦁", "خط 🦅"])
    await update.message.reply_text(f"🪙 سکس پرتاب: {result}")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "دو تا متفرقه تو اتاق تاریک...",
        "یه روز یه برنامه‌نویس...",
        "دو تا null تو اتاق...",
        "یه روز یه توسعه‌دهنده..."
    ]
    await update.message.reply_text(random.choice(jokes))

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("coin", coin))
    application.add_handler(CommandHandler("joke", joke))
    
    application.run_polling()

if __name__ == "__main__":
    main()
