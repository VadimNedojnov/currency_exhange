from django.forms import Form, EmailField, CharField
from django.conf import settings


from account.tasks import send_email_async
from account.models import Contact


# class ContactForm(Form):
#     email = EmailField()
#     subject = CharField()
#     text = CharField()
#
#     def save(self):
#         data = self.cleaned_data
#         subject = data['subject']
#         message = data['text']
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [data['email'], ]
#         result = send_email_async.delay(subject, message, from_email, recipient_list)
#         for i in range(len(recipient_list)):
#             email_to_db = Contact.objects.create(email=recipient_list[i], title=subject, text=message)
