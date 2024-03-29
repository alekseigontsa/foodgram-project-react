from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    admin = 'admin'
    user = 'user'
    CHOICES_ROLE = [
        (admin, 'Администратор'),
        (user, 'Пользователь'),
    ]
    email = models.EmailField(
        _('email'),
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=150)
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=15,
        choices=CHOICES_ROLE,
        default=user,
    )
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [models.UniqueConstraint(
            fields=('username', 'email'),
            name='Поля `email` и `username` должны быть уникальными.'), ]
