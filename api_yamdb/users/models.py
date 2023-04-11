from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import reg_validator

USER_USERNAME_MAX_LEN = 150
USER_EMAIL_MAX_LEN = 254
USER_ROLE_MAX_LEN = 10
USER_CODE_MAX_LEN = 100
USER_NAME_MAX_LEN = 150


class User(AbstractUser):
    """Модель пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USER_USERNAME_MAX_LEN,
        unique=True,
        validators=(reg_validator,)
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=USER_EMAIL_MAX_LEN,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        default=USER,
        max_length=USER_ROLE_MAX_LEN
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=USER_CODE_MAX_LEN,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_NAME_MAX_LEN,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_NAME_MAX_LEN,
        blank=True,
    )

    @property
    def is_admin(self):
        """Проверка пользователя на администратора."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка пользователя на модератора."""
        return self.role == self.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
