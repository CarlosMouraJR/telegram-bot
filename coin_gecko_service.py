import requests

class CoinGeckoService:
    def __init__(self, base_url="https://api.coingecko.com/api/v3"):
        self.base_url = base_url

    def get_price(self, coin_id, currency="usd"):
        url = f"{self.base_url}/simple/price?ids={coin_id}&vs_currencies={currency}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data.get(coin_id, {}).get(currency)
        else:
            print(f"Erro na resposta da API ao obter preço de {coin_id}: {response.json()}")
            return None
