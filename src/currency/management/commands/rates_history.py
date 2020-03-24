from decimal import Decimal
import requests
import datetime


from django.core.management.base import BaseCommand


from currency.models import Rate
from currency import model_choices as mch


class Command(BaseCommand):
    help = 'This command adds rates for the last four years to the DB'

    def handle(self, *args, **options):
        for i in range(1, 1460):
            d = datetime.timedelta(days=-i)
            date = datetime.datetime.now() + d
            date_in_list = str(date).split(' ')[0].split('-')
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date=' \
                  f'{date_in_list[2]}.{date_in_list[1]}.{date_in_list[0]}'
            response_privat = requests.get(url).json()
            r_json = response_privat['exchangeRate']
            for rate in r_json:
                if 'currency' in rate:
                    if rate['currency'] in {'USD', 'EUR'}:
                        currency = mch.CURR_USD if rate['currency'] == 'USD' else mch.CURR_EUR
                        date_time_str = response_privat['date']
                        if 'purchaseRate' and 'saleRate' in rate:
                            rate_kwargs = {
                                'currency': currency,
                                'buy': Decimal(rate['purchaseRate']),
                                'sale': Decimal(rate['saleRate']),
                                'source': mch.SR_PRIVAT,
                                'created': datetime.datetime.strptime(date_time_str, '%d.%m.%Y')
                            }
                        else:
                            rate_kwargs = {
                                'currency': currency,
                                'buy': Decimal(rate['purchaseRateNB']),
                                'sale': Decimal(rate['saleRateNB']),
                                'source': mch.SR_PRIVAT,
                                'created': datetime.datetime.strptime(date_time_str, '%d.%m.%Y')
                            }
                        new_rate = Rate(**rate_kwargs)
                        new_rate.save()
