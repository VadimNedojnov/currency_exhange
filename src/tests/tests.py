import pytest
from uuid import uuid4
from decimal import Decimal


from django.urls import reverse
from django.core import mail

from account.models import Contact
from currency.models import Rate
from currency.tasks import _privat, _mono
from account.tasks import send_activation_code_async


def test_sanity():
    assert 200 == 200


def test_index_page(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


def test_rates_not_auth(client):
    url = reverse('api-currency:rates')
    response = client.get(url)
    assert response.status_code == 401
    resp_j = response.json()
    assert len(resp_j) == 1
    assert resp_j['detail'] == 'Authentication credentials were not provided.'


def test_rates_auth(api_client, user):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.login(user.username, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


def test_get_rates(api_client, user):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 200

    # response = api_client.put(url + id, data={}, format='json')
    # response = api_client.delete(url + id, data={}, format='json')


def test_post_rates(api_client, user):
    url = reverse('api-currency:rates')
    rates_1_len = len(Rate.objects.all())
    response = api_client.post(
        url,
        data={
            "sale": 23.11,
            "currency": 1,
            "source": 1,
            "buy": 23.55
        },
        format='json'
    )
    assert response.status_code == 201
    rates_2_len = len(Rate.objects.all())
    assert rates_2_len == rates_1_len + 1
    rate = Rate.objects.last()
    assert rate.sale == Decimal('23.11')
    assert rate.currency == 1
    assert rate.source == 1
    assert rate.buy == Decimal('23.55')


def test_get_rate(api_client, user):
    rate_id = Rate.objects.last().id
    url = reverse('api-currency:rate', kwargs={'pk': rate_id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['buy'] == '23.55'
    assert response.json()['sale'] == '23.11'
    assert response.json()['get_currency_display'] == 'USD'
    assert response.json()['get_source_display'] == 'Privat Bank'


def test_get_contacts(api_client, user):
    url = reverse('api-currency:contacts')
    response = api_client.get(url)
    assert response.status_code == 200


def test_post_contacts(api_client, user):
    url = reverse('api-currency:contacts')
    contacts_1_len = len(Contact.objects.all())
    response = api_client.post(
        url,
        data={
            'email': 'awdawdawdaw@mail.com',
            'title': 'TestTitle',
            'text': 'TestText'
        },
        format='json'
    )
    assert response.status_code == 201
    contacts_2_len = len(Contact.objects.all())
    assert contacts_2_len == contacts_1_len + 1
    emails = mail.outbox
    contact = Contact.objects.last()
    assert contact.title == emails[-1].subject
    assert contact.text == emails[-1].body
    assert contact.email == emails[-1].recipients()[0]


def test_get_contact(api_client, user):
    contact_id = Contact.objects.last().id
    url = reverse('api-currency:contact', kwargs={'pk': contact_id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['title'] == 'TestTitle'
    assert response.json()['text'] == 'TestText'
    assert response.json()['email'] == 'awdawdawdaw@mail.com'


def test_put_contact(api_client, user):
    contact_id = Contact.objects.last().id
    url = reverse('api-currency:contact', kwargs={'pk': contact_id})
    response = api_client.put(
        url,
        data={
            'email': 'awdawdawdaw|_NEW_|@mail.com',
            'title': 'TestTitle|_NEW_|',
            'text': 'TestText|_NEW_|'
        },
        format='json'
    )
    assert response.status_code == 200
    response_after_change = api_client.get(url)
    assert response_after_change.status_code == 200
    assert response_after_change.json()['title'] == 'TestTitle|_NEW_|'
    assert response_after_change.json()['text'] == 'TestText|_NEW_|'
    assert response_after_change.json()['email'] == 'awdawdawdaw|_NEW_|@mail.com'


def test_patch_contact(api_client, user):
    contact_id = Contact.objects.last().id
    url = reverse('api-currency:contact', kwargs={'pk': contact_id})
    response = api_client.patch(
        url,
        data={
            'title': 'TestTitle|_PATCHED_|',
            'text': 'TestText|_PATCHED_|'
        },
        format='json'
    )
    assert response.status_code == 200
    response_after_change = api_client.get(url)
    assert response_after_change.status_code == 200
    assert response_after_change.json()['title'] == 'TestTitle|_PATCHED_|'
    assert response_after_change.json()['text'] == 'TestText|_PATCHED_|'
    assert response_after_change.json()['email'] == 'awdawdawdaw|_NEW_|@mail.com'


def test_delete_contact(api_client, user):
    contact_id = Contact.objects.last().id
    url = reverse('api-currency:contact', kwargs={'pk': contact_id})
    response = api_client.delete(url)
    assert response.status_code == 405
    assert response.reason_phrase == 'Method Not Allowed'


class Response:    # Class for fake response with .json
    pass


def test_task_privat(mocker):

    def mock():
        response = Response()
        response.json = lambda: [
            {"ccy": "USD", "base_ccy": "UAH", "buy": "27.20", "sale": "27.62"},
            {"ccy": "EUR", "base_ccy": "UAH", "buy": "29.30", "sale": "29.85"},
            {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.31", "sale": "0.36"}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    Rate.objects.all().delete()

    _privat()
    rate = Rate.objects.all()
    assert len(rate) == 2
    assert rate[0].currency == 1
    assert rate[0].buy == Decimal('27.20')
    assert rate[0].sale == Decimal('27.62')
    assert rate[0].source == 1
    assert rate[1].currency == 2
    assert rate[1].buy == Decimal('29.30')
    assert rate[1].sale == Decimal('29.85')
    assert rate[1].source == 1
    Rate.objects.all().delete()


def test_task_nomo(mocker):

    def mock():
        response = Response()
        response.json = lambda: [
            {"currencyCodeA": 840, "currencyCodeB": 980, "rateBuy": 27.35, "rateSell": 27.61},
            {"currencyCodeA": 978, "currencyCodeB": 980, "rateBuy": 29.45, "rateSell": 29.83},
            {"currencyCodeA": 643, "currencyCodeB": 980, "rateBuy": 0.315, "rateSell": 0.36}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _mono()
    rate = Rate.objects.all()
    assert len(rate) == 2
    assert rate[0].currency == 1
    assert rate[0].buy == Decimal('27.35')
    assert rate[0].sale == Decimal('27.61')
    assert rate[0].source == 2
    assert rate[1].currency == 2
    assert rate[1].buy == Decimal('29.45')
    assert rate[1].sale == Decimal('29.83')
    assert rate[1].source == 2
    Rate.objects.all().delete()


def test_send_email():
    send_activation_code_async.delay(1, str(uuid4()))
    emails = mail.outbox
    assert len(emails) == 1

    email = mail.outbox[0]
    assert email.subject == 'Your activation code'

# tests for ContactUs API, GET list, create (POST), for object [GET, PUT, PATCH, DELETE]

# 0. email = 'awdawdawdaw@mail.com'
# 1. client.post('/registration/'. data={email: email})
# 2. User.objects.get(email=email).uuid, emails = mail.outbox.
# 3. client.post('/registration/complete/'. data={uuid: uuid})
# 4. user LOGIN!
