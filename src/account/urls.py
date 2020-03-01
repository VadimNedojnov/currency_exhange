from django.urls import path


from account.views import SignUp


app_name = 'account'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', SignUp.as_view(), name='registration'),
]
