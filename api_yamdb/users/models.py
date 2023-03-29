from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )

    @property
    def is_admin(self):
        """Проверка пользователя на администратора."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка пользователя на модератора."""
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
