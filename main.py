import json
import asyncio
from telegram_service import TelegramService
from coin_gecko_service import CoinGeckoService


async def monitor_prices(service, telegram_service):
    messages = []

    price_btc = service.get_price("bitcoin", currency="usd")
    price_usdt = service.get_price("tether", currency="brl")

    if price_btc is not None:
        messages.append(f"Preço atual do BTC/USDT: ${price_btc:.2f}")

    if price_usdt is not None:
        messages.append(f"Preço atual do USDT/BRL: R${price_usdt:.2f}")

    return messages

async def main():
    telegram_service = TelegramService()
    service = CoinGeckoService()

    messages = await monitor_prices(service, telegram_service)
    for message in messages:
        await telegram_service.send_alert(message)

def handler(event, context):
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Monitoring prices started'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
