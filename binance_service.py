import requests
import os

class BinanceService:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3/ticker/price"

    def get_price(self, symbol):
        url = f"{self.base_url}?symbol={symbol}"
        try:
            response = requests.get(url)
            data = response.json()
            if 'price' in data:
                return float(data['price'])
            else:
                print(f"Erro na resposta da API ao obter preço do {symbol}: {data}")
                return None
        except Exception as e:
            print(f"Erro ao obter o preço do {symbol}: {e}")
            return None
