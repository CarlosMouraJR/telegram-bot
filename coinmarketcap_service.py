import requests
import os

class CoinmarketcapService:
    def __init__(self):
        self.coinmarketcap_api_key = os.getenv('COINMARKETCAP_API_KEY')
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    def get_price(self, symbol):
        parameters = {
            'symbol': symbol,
            'convert': 'USD' if symbol == 'BTC' else 'BRL'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.coinmarketcap_api_key,
        }
        try:
            response = requests.get(self.url, headers=headers, params=parameters)
            data = response.json()
            if 'data' in data and symbol in data['data']:
                if symbol == 'BTC':
                    return float(data['data']['BTC']['quote']['USD']['price'])
                elif symbol == 'USDT':
                    return float(data['data']['USDT']['quote']['BRL']['price'])
            else:
                print(f"Erro na resposta da API ao obter preço do {symbol}: {data}")
                return None
        except Exception as e:
            print(f"Erro ao obter o preço do {symbol}: {e}")
            return None
