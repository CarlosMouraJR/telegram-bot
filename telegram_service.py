import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

class TelegramService:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.bot = Bot(token=self.telegram_token)
        self.sent_message_ids = []

    async def delete_all_messages(self):
        for message_id in self.sent_message_ids:
            try:
                await self.bot.delete_message(chat_id=self.chat_id, message_id=message_id)
                print(f"Mensagem {message_id} deletada com sucesso.")
            except Exception as e:
                print(f"Erro ao deletar mensagem {message_id}: {e}")

    async def send_alert(self, message):
        try:
            sent_message = await self.bot.send_message(chat_id=self.chat_id, text=message)
            print(f"Mensagem enviada via Telegram: {message}")
            self.sent_message_ids.append(sent_message.message_id)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
