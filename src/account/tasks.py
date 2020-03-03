from celery import shared_task


from django.core.mail import send_mail


@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def print_word():
    print('Hello from Celery Beat!')


@shared_task
def send_email_async(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
