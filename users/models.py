from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    модель пользователя сервиса
    """
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["last_name", "first_name"]
        permissions = [('can_block_user', 'Can block and unblock users'), ]


class UsersControl(models.Model):
    """
    механизм управления всеми пользователями как единым целым (мне так удобно)
    """
    users = models.ManyToManyField(CustomUser, verbose_name="Пользователи, которым можно заходить в приложение")

    class Meta:
        verbose_name = "Управление пользователями"
