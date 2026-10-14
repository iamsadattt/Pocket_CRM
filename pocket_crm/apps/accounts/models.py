from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Extending the standard Django User
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    timezone = models.CharField(max_length=50, default='UTC', blank=True)

    # Use email for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email
