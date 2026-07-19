import logging
import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956668860:AAHzvS0-eBvMAPpVNQsxIr8...")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_menu_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 جستجوی آهنگ", callback_data='search')],
        [InlineKeyboardButton("📋 پلی‌لیست من", callback_data='playlist'),
         InlineKeyboardButton("❓ راهنما", callback_data='help')]
    ])

def download_audio(youtube_url, output_path="song.mp3"):
    try:
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", output_path,
            youtube_url
        ]
        subprocess.run(cmd, check=True, timeout=120)
        return True
    except:
        return False

def search_youtube(query):
    try:
        cmd = [
            "yt-dlp",
            "--default-search", "ytsearch5",
            "--print", "%(title)s|%(id)s|%(duration)s",
            "-I", "1:5",
            f"ytsearch5:{query}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                parts = line.split('|', 2)
                if len(parts) == 3:
                    title, video_id, duration = parts
                    videos.append({
                        "title": title,
                        "url": f"https://youtube.com/watch?v={video_id}",
                        "duration": duration
                    })
        return videos
    except:
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎵 *ربات موزیک پلیر ایرانی*\n\n"
        "🔍 نام آهنگ یا خواننده رو بنویس\n"
        "مثال: `محسن چاوشی` یا `شهرام ناظری`\n\n"
        "✨ از یوتیوب جستجو و دانلود می‌کنم"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=get_menu_buttons(), parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(text, reply_markup=get_menu_buttons(), parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 *راهنما*\n\n"
        "🔍 *جستجو:* نام آهنگ یا خواننده بنویس\n"
        "📥 *دانلود:* ربات آهنگ رو دانلود و می‌فرسته\n"
        "⏯️ *پلی/استاپ:* با دکمه کنترل کن\n\n"
        "⚠️ *نکته:* دانلود از یوتیوب ممکنه کند باشه"
    )
    keyboard = [[InlineKeyboardButton("🏠 منوی اصلی", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    
    if not query or query.startswith('/'):
        return
    
    searching_msg = await update.message.reply_text("🔍 در حال جستجو در یوتیوب...")
    
    results = search_youtube(query)
    
    if not results:
        await searching_msg.edit_text(
            "❌ آهنگی پیدا نشد!\n\n"
            "🔍 یه کلمه دیگه امتحان کن",
            reply_markup=get_menu_buttons()
        )
        return
    
    keyboard = []
    text = "🎵 *نتایج جستجو:*\n\n"
    
    for i, video in enumerate(results[:5], 1):
        title = video["title"]
        duration = video["duration"]
        url = video["url"]
        
        try:
            duration_int = int(duration)
            minutes = duration_int // 60
            seconds = duration_int % 60
            time_str = f"{minutes}:{seconds:02d}"
        except:
            time_str = "?"
        
        text += f"{i}. *{title}*\n"
        text += f"   ⏱️ {time_str}\n\n"
        
        keyboard.append([InlineKeyboardButton(f"▶️ {title[:30]}", callback_data=f'download_{i}_{url}')])
    
    keyboard.append([InlineKeyboardButton("🔄 جستجوی دیگر", callback_data='search')])
    
    await searching_msg.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'search':
        await query.edit_message_text(
            "🔍 *نام آهنگ یا خواننده رو بنویس:*\n\n"
            "مثال: `همایون شجریان`",
            parse_mode='Markdown'
        )
    elif data == 'menu':
        await start(update, context)
    elif data == 'help':
        await help_command(update, context)
    elif data.startswith('download_'):
        parts = data.split('_', 2)
        if len(parts) >= 3:
            url = parts[2]
            
            downloading_msg = await query.edit_message_text(
                "⬇️ در حال دانلود...\n"
                "⏳ ممکنه چند ثانیه طول بکشه",
                parse_mode='Markdown'
            )
            
            output_file = f"song_{query.from_user.id}.mp3"
            success = download_audio(url, output_file)
            
            if success and os.path.exists(output_file):
                with open(output_file, 'rb') as audio_file:
                    await query.message.reply_audio(
                        audio=audio_file,
                        caption="🎵 *آهنگ دانلود شد!*\n\n✨ لذت ببر",
                        parse_mode='Markdown'
                    )
                
                os.remove(output_file)
                await downloading_msg.delete()
            else:
                await downloading_msg.edit_text(
                    f"❌ خطا در دانلود!\n\n"
                    f"🔗 [لینک یوتیوب]({url})\n\n"
                    f"🔄 دوباره امتحان کن",
                    parse_mode='Markdown'
                )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == "__main__":
    main()
