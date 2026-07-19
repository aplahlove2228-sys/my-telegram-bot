																	import logging
import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956666860:AAHzvS0-eBvMAPpVNQsxIr80jKC8wdmxrtI")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "من ربات دانلود YouTube هستم!\n\n"
        "🔗 لینک ویدیوی YouTube رو بفرست تا برات دانلود کنم!\n\n"
        "⚠️ محدودیت: ویدیوهای زیر ۵۰ مگابایت"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 راهنما:\n\n"
        "1️⃣ لینک ویدیوی YouTube رو کپی کن\n"
        "2️⃣ اینجا Paste کن و بفرست\n"
        "3️⃣ صبر کن تا دانلود بشه\n\n"
        "⚠️ محدودیت: ویدیوهای زیر ۵۰ مگابایت"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # بررسی لینک YouTube
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ لطفاً یه لینک معتبر YouTube بفرست!")
        return
    
    # پیام در حال دانلود
    status_message = await update.message.reply_text("⏳ در حال دانلود... لطفاً صبر کنید")
    
    try:
        # تنظیمات دانلود با User-Agent مرورگر
        ydl_opts = {
            'format': 'best[filesize<50M]',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            'cookiefile': None,  # کوکی نمی‌خواد
            'nocheckcertificate': True,
        }
        
        # دانلود
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # ارسال ویدیو
            await status_message.edit_text("✅ دانلود تموم شد! در حال ارسال...")
            
            with open(filename, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"🎬 {info.get('title', 'ویدیو')}\n\n✅ دانلود شد!"
                )
            
            # پاک کردن فایل
            if os.path.exists(filename):
                os.remove(filename)
            
            await status_message.delete()
            
    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            await status_message.edit_text(
                "❌ YouTube ربات رو شناسایی کرد!\n\n"
                "لطفاً از ویدیوهای کوتاه‌تر یا لینک‌های دیگه استفاده کنید.\n"
                "یا لینک رو با فرمت زیر بفرست:\n"
                "`https://www.youtube.com/watch?v=VIDEO_ID`"
            )
        else:
            await status_message.edit_text(f"❌ خطا: {error_msg}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    logger.info("🤖 ربات دانلود YouTube در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()    ContextTypes.DEFAULT_TYPE): jokes = [
        "چرا کامپیوتر به دکتر رفت؟ چون ویروس 
        گرفته بود! 😂", "برنامه‌نویس وارد رستوران 
        شد. گارسون پرسید: چی میل دارید؟ گفت: 
        منوی اصلی رو نشون بده! 😅", "چرا جاوا 
        اسکریپت به جاوا رفت؟ چون null بود! 🤣", 
        "برنامه‌نویس‌ها چرا تاریکی رو دوست دارن؟ 
        چون نور باعث باگ میشه! 💡",
    ] await 
    update.message.reply_text(random.choice(jokes)) 
    application.add_handler(CommandHandler("dice", 
    dice)) 
    application.add_handler(CommandHandler("coin", 
    coin)) 
    application.add_handler(CommandHandler("joke", 
    joke)) 
    application.add_handler(MessageHandler(filters.TEXT 
    & ~filters.COMMAND, echo)) 
    application.run_polling()
