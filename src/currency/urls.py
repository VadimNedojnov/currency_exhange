from django.urls import path


from currency.views import rates_list


app_name = 'currency'

urlpatterns = [
    path('rates-list/', rates_list, name='rates_list'),
]
