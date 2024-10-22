import os
import asyncio
from dotenv import load_dotenv
from telegram_service import TelegramService
from coinmarketcap_service import CoinmarketcapService
from binance_service import BinanceService

load_dotenv()

binance_source = os.getenv('BINANCE_SOURCE', 'True') == 'True'
interval = int(os.getenv('INTERVAL', 20))

async def monitor_prices(service, telegram_service, interval=500):
    while True:


        price_btc = service.get_price("BTCUSDT")
        price_usdt = service.get_price("USDTBRL")

        if price_btc is not None:
            alert_message_btc = f"Preço atual do BTC/USDT: ${price_btc:.2f}"
            await telegram_service.send_alert(alert_message_btc)

        if price_usdt is not None:
            alert_message_usdt = f"Preço atual do USDT/BRL: R${price_usdt:.2f}"
            await telegram_service.send_alert(alert_message_usdt)

        await asyncio.sleep(interval)
        await telegram_service.delete_all_messages()
        await asyncio.sleep(interval)

async def main():
    telegram_service = TelegramService()
    service = BinanceService() if binance_source else CoinmarketcapService()

    await monitor_prices(service, telegram_service, interval=interval)

if __name__ == "__main__":
    asyncio.run(main())
