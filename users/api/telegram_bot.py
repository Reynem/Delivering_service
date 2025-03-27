from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


class TelegramBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_code)
        )

    async def start(self, update: Update, context):
        chat_id = update.effective_chat.id
        await update.message.reply_text(
            f"🆔 Ваш Chat ID: {chat_id}\n"
            "Используйте его для привязки аккаунта в личном кабинете"
        )

    async def handle_code(self, update: Update, context):
        code = update.message.text
        chat_id = update.effective_chat.id

    async def send_message(self, chat_id: int, text: str):
        await self.application.bot.send_message(
            chat_id=chat_id,
            text=text
        )

    async def run(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()