from uuid import uuid4
from datetime import datetime


from django.db import models
from django.contrib.auth.models import AbstractUser


from account.tasks import send_activation_code_async


def avatar_path(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    f = str(uuid4())
    filename = f'{f}.{ext}'
    return '/'.join(['avatar', str(instance.id), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)
    street = models.CharField(max_length=100, null=True, blank=True, default=None)
    city = models.CharField(max_length=20, null=True, blank=True, default=None)
    index = models.CharField(max_length=10, null=True, blank=True, default=None)
    phone = models.CharField(max_length=20)
    person_description = models.CharField(max_length=1024, null=True, blank=True, default=None)
    linkedin_link = models.CharField(max_length=200, null=True, blank=True, default=None)
    githab_link = models.CharField(max_length=200, null=True, blank=True, default=None)
    twitter_link = models.CharField(max_length=200, null=True, blank=True, default=None)
    facebook_link = models.CharField(max_length=200, null=True, blank=True, default=None)


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    # code = models.CharField(max_length=128)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)

    # def save(self, *args, **kwargs):
    #     self.code = ... # GENERATE CODE
    #     super().save(*args, **kwargs)
