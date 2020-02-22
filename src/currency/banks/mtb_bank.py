from decimal import Decimal
from bs4 import BeautifulSoup


import requests


from currency.models import Rate
from currency import model_choices as mch


def _mtb():
    url = 'https://mtb.ua/'
    response_mtb = requests.get(url)
    soup = BeautifulSoup(response_mtb.content, 'html.parser')
    items = soup.find_all('div', attrs={"class": "exchange-value_item"})
    currencies = {
        'USD': [],
        'EUR': []
    }
    for i in items:
        curr = i.find_all('div', attrs={"class": "exchange-value_currency"})[0].contents[0].strip()
        value = i.find_all('span', attrs={"class": "exchange-value_num"})[0].contents[0].strip()
        currencies[curr].append(value) if curr in {'USD', 'EUR'} else True
    for i in currencies:
        currency = mch.CURR_USD if i == 'USD' else mch.CURR_EUR
        rate_kwargs = {
            'currency': currency,
            'buy': Decimal(currencies[i][0]),
            'sale': Decimal(currencies[i][1]),
            'source': mch.SR_MTB,
        }
        new_rate = Rate(**rate_kwargs)
        last_rate = Rate.objects.filter(currency=currency, source=mch.SR_MTB).last()
        if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
            new_rate.save()
