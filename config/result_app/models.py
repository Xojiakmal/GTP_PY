from django.db import models
from group_app.models import Groups
from main_app.models import Users

# Create your models here.
class Matches(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True, null=True)
    result = models.IntegerField(null=True)
    status = models.CharField(max_length=10, default="processing")