from celery import shared_task


from django.core.mail import send_mail
from django.urls import reverse


@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def print_word():
    print('Hello from Celery Beat!')


@shared_task
def send_email_async(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)


@shared_task()
def send_activation_code_async(email_to, code):
    path = reverse('account:activate', args=(code, ))

    send_mail(
        'Your activation code',
        f'http://127.0.0.1:8000{path}',
        'xperia.vad1@gmail.com',
        [email_to],
        fail_silently=False,
    )


@shared_task()
def send_sms_code_async(phone, sms_code):
    send_mail(
        'Your activation code',
        sms_code,
        'xperia.vad1@gmail.com',
        'xperia.vad1@gmail.com',
        fail_silently=False,
    )
