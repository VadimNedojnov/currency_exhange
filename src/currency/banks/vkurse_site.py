from decimal import Decimal
from bs4 import BeautifulSoup
import json


import requests


from currency.models import Rate
from currency import model_choices as mch


def _vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response_vkurse = requests.get(url)
    soup = BeautifulSoup(response_vkurse.content, 'html.parser')
    new_dictionary = json.loads(str(soup))
    for i in new_dictionary:
        if i in {'Dollar', 'Euro'}:
            currency = mch.CURR_USD if i == 'Dollar' else mch.CURR_EUR
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(new_dictionary[i]['buy']),
                'sale': Decimal(new_dictionary[i]['sale']),
                'source': mch.SR_VKURSE,
            }
            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_VKURSE).last()
            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()
