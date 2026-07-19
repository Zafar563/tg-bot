import httpx
import telebot
from telebot import types
from currency import get_usd_rate, parse_amount, is_numeric_amount, convert_uzs_to_usd
from prayer import get_prayer_times, format_prayer_times
from weather import format_openweathermap_report

BOT_TOKEN = "8640604721:AAFJbDDqek0c-FDP45kcdfo3iTrk2jakBpA"
API_KEY = "9e8d4bb64eb8b8161a1df865bdee0707"

bot = telebot.TeleBot(BOT_TOKEN)


def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_weather = types.KeyboardButton("🌤 Ob-havo")
    btn_currency = types.KeyboardButton("🧮 Valyuta konvertori")
    btn_prayer = types.KeyboardButton("🕋 Namoz vaqtlari")
    markup.add(btn_weather, btn_currency)
    markup.add(btn_prayer)
    return markup


def get_regions_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    regions = [
        "Toshkent", "Samarqand", "Buxoro",
        "Andijon", "Namangan", "Farg'ona",
        "Xiva", "Qarshi", "Nukus",
        "Jizzax", "Navoiy", "Termiz"
    ]
    buttons = [types.KeyboardButton(r) for r in regions]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("⬅️ Ortga"))
    return markup


def process_weather_step(message):
    if message.text == "⬅️ Ortga":
        bot.send_message(message.chat.id, "🏠 Asosiy menyu", reply_markup=get_main_keyboard())
        return
    if message.text in ["🌤 Ob-havo", "🧮 Valyuta konvertori", "🕋 Namoz vaqtlari"]:
        handle_menu_selection(message)
        return
    get_weather(message)


def process_currency_step(message):
    if message.text == "⬅️ Ortga":
        bot.send_message(message.chat.id, "🏠 Asosiy menyu", reply_markup=get_main_keyboard())
        return
    if message.text in ["🌤 Ob-havo", "🧮 Valyuta konvertori", "🕋 Namoz vaqtlari"]:
        handle_menu_selection(message)
        return
    amount = parse_amount(message.text)
    if amount is None or amount <= 0:
        msg = bot.reply_to(
            message,
            "❌ **Noto'g'ri summa kiritildi.**\n"
            "Iltimos, faqat musbat son kiriting (masalan: `100000`):",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_currency_step)
        return
    processing_msg = bot.reply_to(message, "⏳ Kurs hisoblanmoqda...")
    report = convert_uzs_to_usd(amount)
    bot.edit_message_text(report, chat_id=processing_msg.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')


def handle_menu_selection(message):
    text = message.text
    if text == "🌤 Ob-havo":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("⬅️ Ortga"))
        msg = bot.send_message(
            message.chat.id,
            "🌤 **Ob-havo ma'lumotlarini olish uchun shahar nomini kiriting:**\n(Masalan: `Tashkent`, `Samarkand` yoki `London`)",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_weather_step)
    elif text == "🧮 Valyuta konvertori":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("⬅️ Ortga"))
        msg = bot.send_message(
            message.chat.id,
            "🧮 **O'zbek so'midagi (UZS) summani kiriting:**\n(Masalan: `150000` yoki `100 000` so'm)",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_currency_step)
    elif text == "🕋 Namoz vaqtlari":
        bot.send_message(
            message.chat.id,
            "🕋 **Namoz vaqtlarini bilish uchun hududni tanlang:**",
            reply_markup=get_regions_keyboard()
        )


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **Salom! Ob-havo, Valyuta konvertori va Namoz vaqtlari botiga xush kelibsiz!**\n\n"
        "Ushbu bot orqali siz pastdagi menyu tugmalaridan foydalanib o'zingizga kerakli ma'lumotlarni tezkor olishingiz mumkin.\n\n"
        "Tugmalardan birini bosing va bot yo'riqnomalariga rioya qiling. 🏠"
    )
    bot.reply_to(message, welcome_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')


@bot.message_handler(commands=['namoz'])
def namoz_command_handler(message):
    parts = message.text.strip().split(maxsplit=1)
    region = parts[1].strip() if len(parts) >= 2 else "Toshkent"
    processing_msg = bot.reply_to(message, f"⏳ {region} uchun namoz vaqtlari yuklanmoqda...")
    data = get_prayer_times(region)
    if not data:
        bot.edit_message_text(
            f"❌ **{region}** bo'yicha namoz vaqtlarini yuklab bo'lmadi.\n"
            f"Iltimos, hudud nomini to'g'ri kiritganingizni tekshiring (masalan: `Toshkent`, `Samarqand`).",
            chat_id=processing_msg.chat.id,
            message_id=processing_msg.message_id,
            parse_mode='Markdown'
        )
        return
    report = format_prayer_times(data)
    bot.edit_message_text(report, chat_id=processing_msg.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')


@bot.message_handler(commands=['usd'])
def usd_command_handler(message):
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "❌ **Iltimos, summani kiriting.**\nMasalan: `/usd 100000`", parse_mode='Markdown')
        return
    amount = parse_amount(parts[1])
    if amount is None or amount <= 0:
        bot.reply_to(message, "❌ **Noto'g'ri summa kiritildi.**\nIltimos, faqat musbat son kiriting.", parse_mode='Markdown')
        return
    processing_msg = bot.reply_to(message, "⏳ Kurs hisoblanmoqda...")
    report = convert_uzs_to_usd(amount)
    bot.edit_message_text(report, chat_id=processing_msg.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')


@bot.message_handler(func=lambda message: is_numeric_amount(message.text))
def usd_direct_handler(message):
    amount = parse_amount(message.text)
    processing_msg = bot.reply_to(message, "⏳ Kurs hisoblanmoqda...")
    report = convert_uzs_to_usd(amount)
    bot.edit_message_text(report, chat_id=processing_msg.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text in ["🌤 Ob-havo", "🧮 Valyuta konvertori", "🕋 Namoz vaqtlari"])
def menu_handler(message):
    handle_menu_selection(message)


@bot.message_handler(func=lambda message: message.text == "⬅️ Ortga")
def back_handler(message):
    bot.send_message(message.chat.id, "🏠 Asosiy menyu", reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda message: message.text in [
    "Toshkent", "Samarqand", "Buxoro", "Andijon", "Namangan",
    "Farg'ona", "Xiva", "Qarshi", "Nukus", "Jizzax", "Navoiy", "Termiz"
])
def regional_prayer_handler(message):
    region = message.text
    processing_msg = bot.reply_to(message, f"⏳ {region} uchun namoz vaqtlari yuklanmoqda...")
    data = get_prayer_times(region)
    if not data:
        bot.edit_message_text(
            f"❌ **{region}** bo'yicha namoz vaqtlarini yuklab bo'lmadi.\nIltimos keyinroq qaytadan urinib ko'ring.",
            chat_id=processing_msg.chat.id,
            message_id=processing_msg.message_id,
            parse_mode='Markdown'
        )
        return
    report = format_prayer_times(data)
    bot.edit_message_text(report, chat_id=processing_msg.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text.strip()
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=uz"
        with httpx.Client() as client:
            response = client.get(url)
        if response.status_code == 401:
            bot.reply_to(message, "❌ API kalit faol emas yoki noto'g'ri.")
        elif response.status_code == 404:
            bot.reply_to(message, "❌ Shahar topilmadi. Iltimos, nomni to'g'ri kiriting (masalan: Tashkent, Samarkand).")
        elif response.status_code != 200:
            bot.reply_to(message, "❌ Ob-havo ma'lumotlarini yuklashda xatolik yuz berdi. Keyinroq qayta urinib ko'ring.")
        else:
            data = response.json()
            report = format_openweathermap_report(data)
            bot.reply_to(message, report, parse_mode='Markdown')
    except Exception:
        bot.reply_to(message, "❌ Tizimda xatolik yuz berdi. Iltimos keyinroq qaytadan urinib ko'ring.")


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
