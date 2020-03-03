from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
