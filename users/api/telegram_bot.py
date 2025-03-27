from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


async def start(update: Update, context):
    await update.message.reply_text(
        "🔑 Для привязки аккаунта:\n"
        "1. Перейдите в личный кабинет\n"
        "2. Введите ваш Chat ID: " + str(update.message.chat_id)
    )


async def handle_code(update: Update, context):
    code = update.message.text


async def setup_bot(token):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    return application

