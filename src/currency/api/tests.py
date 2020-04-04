from django.test import TestCase
from django.urls import reverse


class ApiRateTestCase(TestCase):
    def setUp(self):     # Запускается перед каждым тестом
        pass

    def tearDown(self) -> None:     # Запускается после каждого теста
        pass

    @classmethod
    def setUpClass(cls):    # выполняется перед всеми тестами в классе
        pass

    @classmethod
    def tearDownClass(cls):    # выполняется после всех тестов в классе
        pass

    def test_get_rates(self):
        headers = {
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg2NjA3NDg4LCJqdGkiOiI2ODhmODNjMTBkM2U0ZGU0ODQyYWZiNjM3NmE3NGZiNyIsInVzZXJfaWQiOjF9.vgdMIabwJ_twncF0ACEQNfmXG92oDPl0jp6eQSl3GeM'
        }
        response = self.client.get(reverse('api-currency:rates'), headers=headers)
        print(response.content)
        self.assertEqual(response.status_code, 200)
