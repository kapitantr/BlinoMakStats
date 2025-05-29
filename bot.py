import os
import json
import shutil
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError

# === Logs property ===
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Settings ===
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
DATA_FILE = 'data.json'
BACKUP_FILE = 'data.json.bak'

# === Utilits ===
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Файл данных не найден. Создаётся новый.")
        return {"blin": 0, "mak": 0, "shava": 0, "shash": 0}

def save_data(data):
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE)
        logger.info("Резервная копия данных сохранена.")
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)
    logger.info("Данные обновлены.")

async def try_send_channel(context: ContextTypes.DEFAULT_TYPE, text: str):
    if not CHANNEL_ID:
        logger.warning("CHANNEL_ID не задан. Отправка в канал пропущена.")
        return False
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='Markdown'
        )
        logger.info("Сообщение отправлено в канал.")
        return True
    except TelegramError as e:
        logger.error(f"Ошибка при отправке в канал: {e}")
        return False

def log_user_action(update: Update, command: str):
    user = update.effective_user
    logger.info(f"👤 Пользователь: {user.full_name} | @{user.username} | ID: {user.id} → Команда: /{command}")

# === Food handler ===
async def food_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, food_key: str, emoji: str, name: str, comment: str):
    log_user_action(update, food_key)

    data = load_data()
    data[food_key] += 1
    save_data(data)

    response_text = f"{emoji} {name} зафиксирован!\nВсего: {data[food_key]}"
    channel_text = (
        f"📢 *Обнаружено новое потребление!*\n\n"
        f"{emoji} {name} был съеден.\n"
        f"📊 Всего {name.lower()}ов: *{data[food_key]}*.\n"
        f"{comment}"
    )

    sent = await try_send_channel(context, channel_text)
    await update.message.reply_text(response_text if sent else response_text + "\n⚠️ Не удалось отправить в канал.")

# === Comands ===
async def blin(update, context):
    await food_handler(update, context, "blin", "🥞", "Блин", "🍽️ Кто-то не знает меры...")

async def mak(update, context):
    await food_handler(update, context, "mak", "🍔", "Мак", "👀 Диетолог в панике...")

async def shava(update, context):
    await food_handler(update, context, "shava", "🌯", "Шаурма", "🔥 Острый выбор!")

async def shash(update, context):
    await food_handler(update, context, "shash", "🍢", "ШашлычОК", "😋 Пахнет дымком...")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user_action(update, "stats")
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
    log_user_action(update, "start")
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

# === ТОЧКА ВХОДА ===
def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не задан. Завершение работы.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("blin", blin))
    app.add_handler(CommandHandler("mak", mak))
    app.add_handler(CommandHandler("shava", shava))
    app.add_handler(CommandHandler("shash", shash))
    app.add_handler(CommandHandler("stats", stats))

    logger.info("✅ Бот успешно запущен.")
    try:
        app.run_polling()
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен пользователем (Ctrl+C).")

if __name__ == "__main__":
    main()
