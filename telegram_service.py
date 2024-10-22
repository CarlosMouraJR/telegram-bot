import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

load_dotenv()

class TelegramService:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.application = ApplicationBuilder().token(self.telegram_token).build()
        self.sent_message_ids = []

    async def delete_all_messages(self):
        for message_id in self.sent_message_ids:
            try:
                await self.application.bot.delete_message(chat_id=self.chat_id, message_id=message_id)
                print(f"Mensagem {message_id} deletada com sucesso.")
            except Exception as e:
                print(f"Erro ao deletar mensagem {message_id}: {e}")
        self.sent_message_ids.clear()

    async def send_alert(self, message):
        try:
            sent_message = await self.application.bot.send_message(chat_id=self.chat_id, text=message)
            print(f"Mensagem enviada via Telegram: {message}")
            self.sent_message_ids.append(sent_message.message_id)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    async def start_bot(self):
        await self.application.initialize()
        print("Bot iniciado com sucesso.")
        await self.application.run_polling()
