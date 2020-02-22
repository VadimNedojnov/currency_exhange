from decimal import Decimal
from bs4 import BeautifulSoup
import re


import requests


from currency.models import Rate
from currency import model_choices as mch


def _obmen():
    url = 'https://obmen.dp.ua/'
    response_obmen = requests.get(url)
    soup = BeautifulSoup(response_obmen.content, 'html.parser')
    currencies = {
        'USD': soup.find_all(href=re.compile("usd-uah"))[0].find_all(
            'div', attrs={"class": "currencies__block-num"}),
        'EUR': soup.find_all(href=re.compile("eur-uah"))[0].find_all(
            'div', attrs={"class": "currencies__block-num"})
    }
    for i in currencies:
        currency = mch.CURR_USD if i == 'USD' else mch.CURR_EUR
        rate_kwargs = {
            'currency': currency,
            'buy': Decimal(currencies[i][0].contents[0]),
            'sale': Decimal(currencies[i][1].contents[0]),
            'source': mch.SR_OBMEN,
        }
        new_rate = Rate(**rate_kwargs)
        last_rate = Rate.objects.filter(currency=currency, source=mch.SR_OBMEN).last()
        if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
            new_rate.save()
