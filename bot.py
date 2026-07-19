import logging
import os
import random
import json
from datetime import datetime, date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8956668860:AAHzvS0-eBvMAPpVNQsxIr8...")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

USER_FALS = {}

def load_data():
    global USER_FALS
    try:
        with open('user_fals.json', 'r', encoding='utf-8') as f:
            USER_FALS = json.load(f)
    except:
        USER_FALS = {}

def save_data():
    with open('user_fals.json', 'w', encoding='utf-8') as f:
        json.dump(USER_FALS, f, ensure_ascii=False)

load_data()

HAFEZ_POEMS = [
    {
        "id": 1,
        "title": "غزل شماره ۱",
        "poem": "اگر آن ترک شیرازی به دست آرد دل ما را\nبا سلسلهٔ زُلف، ما را از سر بندد به دلدار\n\nبا خِرامش چو قَدّسیان، نازپروردش چو پریشان\nبه فِدا دادن جان در طَلبِ کاروانسالار",
        "meaning": "این غزل دربارهٔ عشق و دلدادگی است.",
        "audio": "https://example.com/hafez1.mp3",
        "image": "https://example.com/hafez1.jpg"
    },
    {
        "id": 2,
        "title": "غزل شماره ۲",
        "poem": "صبا به لطف بگو آن غَزّالِ رَعنا را\nکه سر به بادِ صبا دادی، بازمَده به ما را\n\nشکایت از لبِ لعلِ تو، گر چه شیرین است لیکن\nزِ عادت بد نپسندم، عَذرِ بدگوها را",
        "meaning": "این غزل دربارهٔ دوری معشوق است.",
        "audio": "https://example.com/hafez2.mp3",
        "image": "https://example.com/hafez2.jpg"
    },
    {
        "id": 3,
        "title": "غزل شماره ۳",
        "poem": "ساقیا برخیز و دردِه جامِ را\nخاک بر سرِ زهدِ فَراموش‌نامِ را\n\nباده بده، شادی بده، غم مخور، راه بده\nدرده راحتِ دلِ غمدیدهٔ ایامِ را",
        "meaning": "این غزل دربارهٔ زندگی و شادی است.",
        "audio": "https://example.com/hafez3.mp3",
        "image": "https://example.com/hafez3.jpg"
    },
    {
        "id": 4,
        "title": "غزل شماره ۴",
        "poem": "دُرَختِ ایمانِ بِی‌بَرگ و بَر، عِشق است\nوین رَهزَنِ عَقل و دین، عِشق است\n\nهر آن کَس کِه بِه دامِ عِشق افتاد\nاز او نِشاط و شادی و سَرور است",
        "meaning": "این غزل دربارهٔ قدرت عشق است.",
        "audio": "https://example.com/hafez4.mp3",
        "image": "https://example.com/hafez4.jpg"
    },
    {
        "id": 5,
        "title": "غزل شماره ۵",
        "poem": "مَی خورَم و مَست و مَلولانَم\nبِه دَورِ مَی و مَست و مَلولانَم\n\nمَن آنِ مَستِ مَحوَم کِه دَر مَی\nنَه نام و نَه نشان دارَم",
        "meaning": "این غزل دربارهٔ حالت مستی و فنا در عشق است.",
        "audio": "https://example.com/hafez5.mp3",
        "image": "https://example.com/hafez5.jpg"
    }
]

FAL_TAABIR = {
    "خوب": [
        "🌟 فال شما خوب است! ایام خوشی در پیش دارید.",
        "✨ نیت شما مستجاب می‌شود.",
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

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🌙 گرفتن فال", callback_data='fal')],
        [InlineKeyboardButton("📖 فال‌های قبلی", callback_data='history'),
         InlineKeyboardButton("❓ راهنما", callback_data='help')],
        [InlineKeyboardButton("🌟 فال روزانه", callback_data='daily_fal')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_fal_buttons(poem_id):
    keyboard = [
        [InlineKeyboardButton("🔊 صوت غزل", callback_data=f'audio_{poem_id}'),
         InlineKeyboardButton("🎴 تصویر", callback_data=f'image_{poem_id}')],
        [InlineKeyboardButton("📤 اشتراک فال", callback_data=f'share_{poem_id}')],
        [InlineKeyboardButton("🔄 فال دیگر", callback_data='fal'),
         InlineKeyboardButton("🏠 منوی اصلی", callback_data='menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌹 *سلام به ربات فال حافظ خوش اومدی!*\n\n"
        "✨ نیت کن و یه فال بگیر\n\n"
        "👇 از دکمه‌ها استفاده کن:"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=get_main_menu(), parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(text, reply_markup=get_main_menu(), parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 *راهنمای ربات فال حافظ*\n\n"
        "🌙 *فال حافظ* - یه غزل تصادفی + تعبیر\n"
        "📖 *فال‌های قبلی* - فال‌هایی که گرفتی\n"
        "🌟 *فال روزانه* - هر روز یه فال (فقط ۱ بار)\n\n"
        "🔊 *صوت غزل* - گوش دادن به غزل\n"
        "🎴 *تصویر* - عکس غزل\n"
        "📤 *اشتراک* - فرستادن فال برای دوست\n\n"
        "✨ قبل از فال، نیت کن!"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 منوی اصلی", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def get_fal(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
    poem = random.choice(HAFEZ_POEMS)
    taabir_type = random.choice(list(FAL_TAABIR.keys()))
    taabir = random.choice(FAL_TAABIR[taabir_type])
    
    if user_id not in USER_FALS:
        USER_FALS[user_id] = []
    
    fal_record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "poem_id": poem["id"],
        "poem_title": poem["title"],
        "taabir": taabir
    }
    USER_FALS[user_id].append(fal_record)
    save_data()
    
    text = (
        f"📜 *{poem['title']}*\n\n"
        f"```\n{poem['poem']}\n```\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"📝 *معنی:*\n{poem['meaning']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔮 *تعبیر فال:*\n{taabir}\n\n"
        f"✨ نیت کنید و صبر کنید..."
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=get_fal_buttons(poem["id"]),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=get_fal_buttons(poem["id"]),
            parse_mode='Markdown'
        )

async def get_daily_fal(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
    today = str(date.today())
    
    if user_id in USER_FALS:
        for fal in reversed(USER_FALS[user_id]):
            if fal.get('type') == 'daily' and fal['date'].startswith(today):
                await update.callback_query.edit_message_text(
                    "⏰ *امروز قبلاً فال گرفتی!*\n\n"
                    "🌙 فال روزانه فقط یک بار در روز\n"
                    "✨ فردا برگرد!",
                    reply_markup=get_main_menu(),
                    parse_mode='Markdown'
                )
                return
    
    poem = random.choice(HAFEZ_POEMS)
    taabir_type = random.choice(list(FAL_TAABIR.keys()))
    taabir = random.choice(FAL_TAABIR[taabir_type])
    
    if user_id not in USER_FALS:
        USER_FALS[user_id] = []
    
    fal_record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "poem_id": poem["id"],
        "poem_title": poem["title"],
        "taabir": taabir,
        "type": "daily"
    }
    USER_FALS[user_id].append(fal_record)
    save_data()
    
    text = (
        f"🌟 *فال روزانه - {today}*\n\n"
        f"📜 *{poem['title']}*\n\n"
        f"```\n{poem['poem']}\n```\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔮 *تعبیر فال:*\n{taabir}\n\n"
        f"✨ روز خوبی داشته باشی!"
    )
    
    await update.callback_query.edit_message_text(
        text,
        reply_markup=get_fal_buttons(poem["id"]),
        parse_mode='Markdown'
    )

async def get_history(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
    if user_id not in USER_FALS or not USER_FALS[user_id]:
        await update.callback_query.edit_message_text(
            "📭 *هنوز فالی نگرفتی!*\n\n"
            "🌙 برو یه فال بگیر",
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )
        return
    
    history = USER_FALS[user_id][-5:]
    text = "📖 *فال‌های قبلی:*\n\n"
    
    for i, fal in enumerate(reversed(history), 1):
        text += f"{i}. {fal['poem_title']} - {fal['date']}\n"
        text += f"   🔮 {fal['taabir'][:50]}...\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 منوی اصلی", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data == 'fal':
        await get_fal(update, context, user_id)
    elif data == 'daily_fal':
        await get_daily_fal(update, context, user_id)
    elif data == 'history':
        await get_history(update, context, user_id)
    elif data == 'help':
        await help_command(update, context)
    elif data == 'menu':
        await start(update, context)
    elif data.startswith('audio_'):
        poem_id = int(data.split('_')[1])
        poem = next((p for p in HAFEZ_POEMS if p['id'] == poem_id), None)
        if poem:
            await query.edit_message_text(
                f"🔊 *صوت {poem['title']}*\n\n"
                f"[🎧 گوش دادن]({poem['audio']})\n\n"
                f"✨ لذت ببر!",
                reply_markup=get_fal_buttons(poem_id),
                parse_mode='Markdown'
            )
    elif data.startswith('image_'):
        poem_id = int(data.split('_')[1])
        poem = next((p for p in HAFEZ_POEMS if p['id'] == poem_id), None)
        if poem:
            await query.edit_message_text(
                f"🎴 *تصویر {poem['title']}*\n\n"
                f"[👁️ مشاهده]({poem['image']})\n\n"
                f"✨ زیباست نه؟",
                reply_markup=get_fal_buttons(poem_id),
                parse_mode='Markdown'
            )
    elif data.startswith('share_'):
        poem_id = int(data.split('_')[1])
        poem = next((p for p in HAFEZ_POEMS if p['id'] == poem_id), None)
        if poem:
            share_text = (
                f"🌹 *فال حافظ*\n\n"
                f"📜 *{poem['title']}*\n\n"
                f"```\n{poem['poem']}\n```\n\n"
                f"✨ از ربات فال حافظ گرفتم!"
            )
            await query.edit_message_text(
                f"📤 *اشتراک فال*\n\n"
                f"متن زیر رو کپی کن و بفرست:\n\n"
                f"```\n{share_text}\n```",
                reply_markup=get_fal_buttons(poem_id),
                parse_mode='Markdown'
            )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == "__main__":
    main()
