from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.
User = get_user_model()
'''
class User(AbstractUser):
    email = models.CharField()

'''

class Titles(models.Model):
    pass


class Category(models.Model):
    pass

class Generes(models.Model):
    pass

class Reviews(models.Model):
    pass
