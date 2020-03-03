from celery import shared_task
from currency.banks.industrial_bank import _industrialbank
from currency.banks.mono_bank import _mono
from currency.banks.mtb_bank import _mtb
from currency.banks.obmen_site import _obmen
from currency.banks.privat_bank import _privat
from currency.banks.vkurse_site import _vkurse


@shared_task()
def parse_rates():
    _privat()
    _mono()
    _vkurse()
    _obmen()
    _mtb()
    _industrialbank()
