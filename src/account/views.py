from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings


from account.models import User, Contact
from account.tasks import send_email_async
# from account.forms import ContactForm


class SignUp(CreateView):
    model = User
    fields = ['username', 'email']
    # form_class = UserCreationForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'


# def contact(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse_lazy('index'))
#     else:
#         form = ContactForm()
#     return render(request,
#                   'contact.html',
#                   context={'form': form})


class ContactCreateView(CreateView):
    model = Contact
    fields = ('email', 'title', 'text')
    template_name = 'contact.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        subject = form.instance.title
        message = form.instance.text
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [form.instance.email, ]
        send_email_async.delay(subject, message, from_email, recipient_list)
        return super().form_valid(form)
