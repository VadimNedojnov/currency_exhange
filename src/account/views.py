from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.conf import settings


from account.models import User, Contact
from account.tasks import send_email_async


class SignUp(CreateView):
    fields = ['username', 'email']
    success_url = reverse_lazy('index')
    template_name = 'registration/registration.html'


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


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', )
    success_url = reverse_lazy('index')
