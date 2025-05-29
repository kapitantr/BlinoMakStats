import os
import json
from dotenv import load_dotenv
from telegram import Update
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
    if sent:
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text(
            response_text + "\n\n⚠️ CHANNEL_ID не задан или ошибка отправки, сообщение не в канал."
        )

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
    if sent:
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text(
            response_text + "\n\n⚠️ CHANNEL_ID не задан или ошибка отправки, сообщение не в канал."
        )

async def shava(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["shava"] += 1
    save_data(data)

    response_text = f"🌯 Шаурма зафиксирована!\nВсего шаурм: {data['shava']}"

    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"🌯 Шаурма была съедена.\n"
        f"📊 Всего шаурм: *{data['shava']}*.\n"
        f"😋 Вкуснятина!"
    )

    sent = await try_send_channel(context, channel_text)
    if sent:
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text(
            response_text + "\n\n⚠️ CHANNEL_ID не задан или ошибка отправки, сообщение не в канал."
        )

async def shash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["shash"] += 1
    save_data(data)

    response_text = f"🍢 ШашлычОК зафиксирован!\nВсего шашлычков: {data['shash']}"

    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"🍢 ШашлычОК был съеден.\n"
        f"📊 Всего шашлычков: *{data['shash']}*.\n"
        f"🔥 Лето рядом!"
    )

    sent = await try_send_channel(context, channel_text)
    if sent:
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text(
            response_text + "\n\n⚠️ CHANNEL_ID не задан или ошибка отправки, сообщение не в канал."
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    stats_text = (
        f"📊 Текущая статистика:\n"
        f"🥞 Блинов: {data['blin']}\n"
        f"🍔 Маков: {data['mak']}\n"
        f"🌯 Шаурм: {data.get('shava', 0)}\n"
        f"🍢 Шашлычков: {data.get('shash', 0)}"
    )

    channel_text = (
        f"📊 Текущая статистика:\n"
        f"🥞 Блинов: {data['blin']}\n"
        f"🍔 Маков: {data['mak']}\n"
        f"🌯 Шаурм: {data.get('shava', 0)}\n"
        f"🍢 Шашлычков: {data.get('shash', 0)}"
    )

    sent = await try_send_channel(context, channel_text)
    if sent:
        await update.message.reply_text(stats_text)
    else:
        await update.message.reply_text(
            stats_text + "\n\n⚠️ CHANNEL_ID не задан или ошибка отправки, сообщение не в канал."
        )

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не задан. Установи переменную окружения и перезапусти скрипт.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("blin", blin))
    app.add_handler(CommandHandler("mak", mak))
    app.add_handler(CommandHandler("shava", shava))
    app.add_handler(CommandHandler("shash", shash))
    app.add_handler(CommandHandler("stats", stats))

    print("✅ Бот запущен. Ожидаю команды...")
    app.run_polling()

if __name__ == "__main__":
    main()
