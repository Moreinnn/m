from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

currency = input("Введите аббревиатуру валюты: ")
currency = currency.upper()

API_KEY = '1d7b4aaa-fa48-4ad8-9551-383cff16e77b'

def get_crypto_data(symbol):

  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'symbol': symbol.upper(),
    'convert': currency 
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    if 'data' in data and symbol.upper() in data['data']:
      crypto_data = data['data'][symbol.upper()]['quote'][currency]
      price = crypto_data['price']
      percent_change_1h = crypto_data['percent_change_1h']
      percent_change_24h = crypto_data['percent_change_24h']
      percent_change_7d = crypto_data['percent_change_7d']

      return {
        'symbol': symbol.upper(),
        'price': price,
        'percent_change_1h': percent_change_1h,
        'percent_change_24h': percent_change_24h,
        'percent_change_7d': percent_change_7d
      }
    else:
      return {'error': 'Криптовалюта не найдена'}

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    return {'error': str(e)}

if __name__ == '__main__':
  symbol = input("Введите символ криптовалюты: ")
  crypto_info = get_crypto_data(symbol)

  if 'error' in crypto_info:
    print(crypto_info['error'])
  else:
    print(f"Цена {crypto_info['symbol']}: {crypto_info['price']:.2f}")
    print(f"Изменение за 1 час: {crypto_info['percent_change_1h']:.2f}%")
    print(f"Изменение за 24 часа: {crypto_info['percent_change_24h']:.2f}%")
    print(f"Изменение за 7 дней: {crypto_info['percent_change_7d']:.2f}%")
