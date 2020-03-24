from django.urls import path


from currency.views import RateListView, RateCSV


app_name = 'currency'

urlpatterns = [
    path('rates-list/', RateListView.as_view(), name='rates-list'),
    path('download/rates', RateCSV.as_view(), name='download-rates'),
]
