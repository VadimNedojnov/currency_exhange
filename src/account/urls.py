from django.urls import path


from account.views import SignUp, ContactCreateView  # , contact


app_name = 'account'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', SignUp.as_view(), name='registration'),
    # path('contact/', contact, name='contact'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
]
