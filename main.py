import os
import asyncio
from dotenv import load_dotenv
from telegram_service import TelegramService
from coin_gecko_service import CoinGeckoService
from binance_service import BinanceService

load_dotenv()

binance_source = os.getenv('BINANCE_SOURCE', True)
interval = int(os.getenv('INTERVAL', 20))

async def monitor_prices(service, telegram_service, interval=500):
    while True:
        price_btc = service.get_price("bitcoin", currency="usd")
        price_usdt = service.get_price("tether", currency="brl")


        if price_btc is not None:
            alert_message_btc = f"Preço atual do BTC/USDT: ${price_btc:.2f}"
            await telegram_service.send_alert(alert_message_btc)

        if price_usdt is not None:
            alert_message_usdt = f"Preço atual do USDT/BRL: R${price_usdt:.2f}"
            await telegram_service.send_alert(alert_message_usdt)

        await asyncio.sleep(interval)

async def main():
    telegram_service = TelegramService()
    service = CoinGeckoService()

    await monitor_prices(service, telegram_service, interval=interval)

# Adiciona a execução assíncrona correta
if __name__ == "__main__":
    asyncio.run(main())
