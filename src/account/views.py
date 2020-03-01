from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


from account.models import User


class SignUp(generic.CreateView):
    model = User
    fields = ['username', 'email']
    # form_class = UserCreationForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'
