import requests
import os
from dotenv import load_dotenv


load_dotenv()


class CurrencyConvertor:

    @classmethod
    def convert_vnd_to_usd(cls, amount):
        EXCHANGE_MONEY_API_KEY = os.getenv('EXCHANGE_MONEY_API_KEY')
        data = requests.get('http://data.fixer.io/api/latest?access_key={}'.format(EXCHANGE_MONEY_API_KEY)).json()
        rates = data['rates']

        from_currency = 'VND'
        to_currency = 'USD'

        initial_amount = amount
        amount = amount / rates[from_currency]

        # limiting the precision to 2 decimal places
        amount = round(amount * rates[to_currency], 2)
        return amount
