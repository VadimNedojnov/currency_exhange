from django.urls import path


from account.views import SignUpView, ContactCreateView, MyProfile, Activate


app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('registration/', SignUpView.as_view(), name='registration'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('profile/<int:pk>', MyProfile.as_view(), name='my-profile'),
    path('activate/', Activate.as_view(), name='activate')
]
