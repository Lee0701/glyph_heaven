from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def clean(self):
        if self.email == '':
            self.email = None
