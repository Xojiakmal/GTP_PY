from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UsersAffinities(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups_id = models.JSONField()
    last_look = models.JSONField()


