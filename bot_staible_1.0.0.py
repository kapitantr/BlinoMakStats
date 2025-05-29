import os
import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"blin": 0, "mak": 0, "shava": 0, "shash": 0}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

async def try_send_channel(context: ContextTypes.DEFAULT_TYPE, text: str):
    if not CHANNEL_ID:
        print("⚠️ CHANNEL_ID не задан, отправка в канал пропущена.")
        return False
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='Markdown'
        )
        return True
    except TelegramError as e:
        print(f"⚠️ Ошибка отправки в канал: {e}")
        return False

async def blin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["blin"] += 1
    save_data(data)

    response_text = f"🥞 Блин зафиксирован!\nВсего блинов: {data['blin']}"
    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"🥞 Блин был съеден.\n"
        f"📊 Всего блинов: *{data['blin']}*.\n"
        f"🍽️ Кто-то не знает меры..."
    )

    sent = await try_send_channel(context, channel_text)
    await update.message.reply_text(response_text if sent else response_text + "\n\n⚠️ Не удалось отправить в канал.")

async def mak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["mak"] += 1
    save_data(data)

    response_text = f"🍔 Мак зафиксирован!\nВсего маков: {data['mak']}"
    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"🍔 Мак зафиксирован.\n"
        f"📊 Всего маков: *{data['mak']}*.\n"
        f"👀 Диетолог в панике..."
    )

    sent = await try_send_channel(context, channel_text)
    await update.message.reply_text(response_text if sent else response_text + "\n\n⚠️ Не удалось отправить в канал.")

async def shava(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["shava"] += 1
    save_data(data)

    response_text = f"🌯 Шаурма зафиксирована!\nВсего шаурмы: {data['shava']}"
    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"🌯 Шаурма была съедена.\n"
        f"📊 Всего шаурмы: *{data['shava']}*.\n"
        f"🔥 Острый выбор!"
    )

    sent = await try_send_channel(context, channel_text)
    await update.message.reply_text(response_text if sent else response_text + "\n\n⚠️ Не удалось отправить в канал.")

async def shash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["shash"] += 1
    save_data(data)

    response_text = f"🍢 ШашлычОК зафиксирован!\nВсего шашлыков: {data['shash']}"
    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"🍢 ШашлычОК был съеден.\n"
        f"📊 Всего шашлыков: *{data['shash']}*.\n"
        f"😋 Пахнет дымком..."
    )

    sent = await try_send_channel(context, channel_text)
    await update.message.reply_text(response_text if sent else response_text + "\n\n⚠️ Не удалось отправить в канал.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    stats_text = (
        f"📊 Текущая статистика:\n"
        f"🥞 Блинов: {data['blin']}\n"
        f"🍔 Маков: {data['mak']}\n"
        f"🌯 Шаурмы: {data['shava']}\n"
        f"🍢 ШашлычОКов: {data['shash']}"
    )
    sent = await try_send_channel(context, stats_text)
    await update.message.reply_text(stats_text if sent else stats_text + "\n\n⚠️ Не удалось отправить в канал.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/blin", "/mak"],
        ["/shava", "/shash"],
        ["/stats"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await update.message.reply_text(
        "Привет! Что сегодня было съедено? 👇",
        reply_markup=reply_markup
    )

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не задан. Установи переменную окружения и перезапусти скрипт.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("blin", blin))
    app.add_handler(CommandHandler("mak", mak))
    app.add_handler(CommandHandler("shava", shava))
    app.add_handler(CommandHandler("shash", shash))
    app.add_handler(CommandHandler("stats", stats))

    print("✅ Бот запущен. Ожидаю команды...")
    app.run_polling()

if __name__ == "__main__":
    main()
