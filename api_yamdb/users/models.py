from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор')
]

class RequiredUser(AbstractUser):


    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default = ROLE_CHOICES[0][0])
    
