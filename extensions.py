import requests
import json
from config import *


class APIException(Exception):
    pass


class APIParser:
    @staticmethod
    def convert(base: str, quote: str, amount: float):
        if base == quote:
            raise APIException(f'Нельзя использовать одинаковую валюту ({base}) для перевода!')

        if base not in keys.keys():
            raise APIException(f'Валюта {base} недоступна!')

        if quote not in keys.keys():
            raise APIException(f'Валюта {quote} недоступна!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать кол-во {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        value = json.loads(r.content)[keys[quote]]
        return value
