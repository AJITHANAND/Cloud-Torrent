from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
