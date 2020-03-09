from django.urls import path


from currency.views import RateListView


app_name = 'currency'

urlpatterns = [
    path('rates-list/', RateListView.as_view(), name='rates-list'),
]
