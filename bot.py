CHANNEL_ID = '@название_твоего_канала'  # Замени на свой

async def blin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["blin"] += 1
    save_data(data)

    text = f"🥞 Блин зафиксирован!\nВсего блинов: {data['blin']}"
    await update.message.reply_text(text)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=(
            f"📢 *Обнаружено новое потребление!*\n\n"
            f"🥞 Блин был съеден.\n"
            f"📊 Всего блинов: *{data['blin']}*.\n"
            f"🍽️ Кто-то не знает меры..."
        ),
        parse_mode='Markdown'
    )

async def mak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data["mak"] += 1
    save_data(data)

    text = f"🍔 Мак зафиксирован!\nВсего маков: {data['mak']}"
    await update.message.reply_text(text)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=(
            f"📢 *Обнаружено новое потребление!*\n\n"
            f"🍔 Мак зафиксирован.\n"
            f"📊 Всего маков: *{data['mak']}*.\n"
            f"👀 Диетолог в панике..."
        ),
        parse_mode='Markdown'
    )
