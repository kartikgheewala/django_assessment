from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """
    Create a user table.
    """
    username = models.CharField(max_length=50, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    auth_token = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        db_table = 'user'
