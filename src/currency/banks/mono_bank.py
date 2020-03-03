from decimal import Decimal


import requests


from currency.models import Rate
from currency import model_choices as mch


def _mono():
    url = 'https://api.monobank.ua/bank/currency'
    response_mono = requests.get(url)
    r_json = response_mono.json()
    for rate in r_json:
        if rate['currencyCodeA'] in {840, 978} and rate['currencyCodeB'] in {980}:
            currency = mch.CURR_USD if rate['currencyCodeA'] == 840 else mch.CURR_EUR
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['rateBuy']).quantize(Decimal("1.00")),
                'sale': Decimal(rate['rateSell']).quantize(Decimal("1.00")),
                'source': mch.SR_MONO,
            }
            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_MONO).last()
            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()
