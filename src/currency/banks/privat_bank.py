from decimal import Decimal


import requests


from currency.models import Rate
from currency import model_choices as mch


def _privat():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response_privat = requests.get(url)
    r_json = response_privat.json()
    for rate in r_json:
        if rate['ccy'] in {'USD', 'EUR'}:   # O(1) if we use list it would be O(n) ('USD', 'EUR')
            # print(rate['ccy'], rate['buy'], rate['sale'])
            currency = mch.CURR_USD if rate['ccy'] == 'USD' else mch.CURR_EUR
            # currency = {
            #     'USD': mch.CURR_USD,
            #     'EUR': mch.CURR_EUR,
            # }[rate['ccy']]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SR_PRIVAT,
            }
            # Rate.objects.create(**rate_kwargs)
            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).last()
            # if last_rate and (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()
            # print(Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).query)
