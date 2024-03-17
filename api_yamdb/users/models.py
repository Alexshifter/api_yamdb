from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (LEN_LIMIT_STR,
                             MAX_LEN_BIO_FIELD,
                             MAX_LEN_EMAIL_FIELD,
                             MAX_LEN_ROLE_FIELD)


class NewUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    ]

    bio = models.TextField(blank=True,
                           max_length=MAX_LEN_BIO_FIELD,
                           verbose_name='биография')
    role = models.CharField(choices=ROLE_CHOICES,
                            default=USER,
                            max_length=MAX_LEN_ROLE_FIELD, verbose_name='роль')
    email = models.EmailField(max_length=MAX_LEN_EMAIL_FIELD,
                              blank=False,
                              unique=True,
                              verbose_name='электронная почта')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_pair_username_email',
            )
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return (f'Пользователь {self.username}, '
                f'роль {self.role}')[:LEN_LIMIT_STR]
