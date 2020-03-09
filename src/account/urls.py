from django.urls import path


from account.views import SignUp, ContactCreateView, MyProfile


app_name = 'account'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', SignUp.as_view(), name='registration'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('profile/<int:pk>', MyProfile.as_view(), name='my-profile'),
]
