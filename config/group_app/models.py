from django.conf import settings
from django.db import models

# Create your models here.
class Groups(models.Model):
    group_name = models.CharField(max_length=50)
    creator_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    tests_id = models.JSONField(null=True)
    duration = models.IntegerField()
    mode = models.CharField(default="public", choices=(('public', 'public'), ('private', 'private')))
    created_at = models.DateTimeField(auto_now_add=True)
