from decimal import Decimal
from bs4 import BeautifulSoup


import requests


from currency.models import Rate
from currency import model_choices as mch


def _industrialbank():
    url = 'https://industrialbank.ua/ua/'
    response_industrialbank = requests.get(url)
    soup = BeautifulSoup(response_industrialbank.content, 'html.parser')
    items = soup.find_all('ul', attrs={"class": "col-sm-9 col-xs-12 exchange-rate-list"})
    currencies = {
        'USD': [],
        'EUR': []
    }
    for i in items:
        all_list = i.find_all('span')
        j = 0
        while j < len(all_list) - 2:
            currencies[all_list[j].contents[0]].append(all_list[j + 1].contents[0])
            j += 2
    for i in currencies:
        currency = mch.CURR_USD if i == 'USD' else mch.CURR_EUR
        rate_kwargs = {
            'currency': currency,
            'buy': Decimal(currencies[i][0]),
            'sale': Decimal(currencies[i][1]),
            'source': mch.SR_INDUSTRIAL,
        }
        new_rate = Rate(**rate_kwargs)
        last_rate = Rate.objects.filter(currency=currency, source=mch.SR_INDUSTRIAL).last()
        if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
            new_rate.save()
