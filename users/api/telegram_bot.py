from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import httpx


class TelegramBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.backend_url = "http://localhost:8000"
        self._setup_handlers()

    def _setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("link", self.handle_link))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_other_text)
        )

    async def start(self, update: Update, context):
        chat_id = update.effective_chat.id
        await update.message.reply_text(
            f"🆔 Ваш Chat ID: {chat_id}\n"
            "Используйте команду /link полученный_код для привязки аккаунта."
        )

    async def handle_link(self, update: Update, context):
        chat_id = update.effective_chat.id
        try:
            temp_token = context.args[0]
            if temp_token:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.backend_url}/user/telegram/link",
                        json={"temp_token": temp_token, "chat_id": chat_id}
                    )
                    response.raise_for_status()
                    await update.message.reply_text("✅ Аккаунт успешно привязан!")
            else:
                await update.message.reply_text("⚠️ Пожалуйста, введите код после команды /link.")
        except IndexError:
            await update.message.reply_text("⚠️ Пожалуйста, введите код после команды /link (например: /link ваш_код).")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                await update.message.reply_text("❌ Неверный или устаревший код.")
            elif e.response.status_code == 400:
                await update.message.reply_text("❌ Ошибка при привязке аккаунта: " + e.response.json().get('detail', 'Неверные данные.'))
            else:
                await update.message.reply_text(f"❌ Произошла ошибка при связывании: {e}")
        except httpx.RequestError as e:
            await update.message.reply_text(f"❌ Не удалось связаться с сервером: {e}")

    async def send_message(self, chat_id: int, text: str):
        try:
            await self.application.bot.send_message(
                chat_id=chat_id,
                text=text
            )
        except Exception as e:
            print(f"[ERROR] Failed to send message to chat {chat_id}: {e}")

    async def handle_other_text(self, update: Update, context):
        await update.message.reply_text("Я понимаю только команду /start ваш_код для привязки аккаунта.")

    async def run(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()