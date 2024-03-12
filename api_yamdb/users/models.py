from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор')
]


class NewUser(AbstractUser):
    bio = models.TextField(blank=True, max_length=100)
    role = models.CharField(choices=ROLE_CHOICES,
                            max_length=20, default=ROLE_CHOICES[0][0])
    confirmation_code = models.CharField(blank=True, max_length=10)
    email = models.EmailField(max_length=254, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_pair_username_email',
            )
        ]
