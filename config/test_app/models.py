from django.db import models

# Create your models here.
class Tests(models.Model):
    content = models.TextField()
    type = models.CharField(max_length=100, choices=(
        ('simpleChoice', 'simpleChoice'),
        ('multiChoice', 'multiChoice')
    ))
    created_at = models.DateTimeField(auto_now_add=True)


class Options(models.Model):
    content = models.TextField()
    test_id = models.ForeignKey(Tests, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# Tests va Options model lari bor. Tests(content, type), Options(content, test_id) bor bular foreignkey bilan ulangan. menga har bir test bir nechta varianti bilan chiqadigan  sorov yozib ber