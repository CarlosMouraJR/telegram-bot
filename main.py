import requests
import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
import streamlit as st

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Token e Chat ID do Telegram obtidos das variáveis de ambiente
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('CHAT_ID')

# URL base da API da Binance obtida da variável de ambiente
binance_api_url = os.getenv('BINANCE_API_URL')

# Cria o bot do Telegram
bot = Bot(token=telegram_token)

# Armazena os IDs das mensagens enviadas
sent_message_ids = []

# Função para deletar todas as mensagens enviadas
async def delete_all_messages():
    for message_id in sent_message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            print(f"Mensagem {message_id} deletada com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar mensagem {message_id}: {e}")

# Função para obter o preço atual do BTC/USDT
def get_btc_price():
    try:
        response = requests.get(f"{binance_api_url}?symbol=BTCUSDT")
        data = response.json()
        if 'price' in data:
            return float(data['price'])
        else:
            print(f"Erro na resposta da API ao obter preço do BTC: {data}")
            return None
    except Exception as e:
        print(f"Erro ao obter o preço do BTC: {e}")
        return None

# Função para obter o preço atual do USDT/BRL
def get_usdt_price():
    try:
        response = requests.get(f"{binance_api_url}?symbol=USDTBRL")
        data = response.json()
        if 'price' in data:
            return float(data['price'])
        else:
            print(f"Erro na resposta da API ao obter preço do USDT: {data}")
            return None
    except Exception as e:
        print(f"Erro ao obter o preço do USDT: {e}")
        return None

# Função para enviar alertas via Telegram
async def send_telegram_alert(message):
    try:
        sent_message = await bot.send_message(chat_id=chat_id, text=message)
        print(f"Mensagem enviada via Telegram: {message}")
        sent_message_ids.append(sent_message.message_id)  # Armazena o ID da mensagem enviada
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

# Função para monitorar os preços
async def monitor_prices(interval=500):
    while True:
        price_btc = get_btc_price()
        price_usdt = get_usdt_price()

        if price_btc is not None:
            alert_message_btc = f"Preço atual do BTC/USDT: ${price_btc:.2f}"
            await send_telegram_alert(alert_message_btc)

        if price_usdt is not None:
            alert_message_usdt = f"Preço atual do USDT/BRL: R${price_usdt:.2f}"
            await send_telegram_alert(alert_message_usdt)

        await asyncio.sleep(interval)
        await delete_all_messages()
        await asyncio.sleep(10)

# Função principal do Streamlit
def main():
    st.title("Monitor de Preços de Criptomoedas")

    if st.button("Iniciar Monitoramento"):
        # Iniciar monitoramento
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(monitor_prices())

if __name__ == "__main__":
    main()
