from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View, ListView
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect


from account.models import User, Contact, ActivationCode
from account.tasks import send_email_async
from account.forms import SignUpForm
from currency.models import Rate


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('index')
    form_class = SignUpForm


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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(
            ActivationCode.objects.select_related('user'),
            code=activation_code, is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')
