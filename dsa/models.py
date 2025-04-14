# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Дополнительные поля
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    email_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.UUIDField(unique=True, verbose_name='Код подтверждения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expiration = models.DateTimeField(verbose_name='Срок действия')

    class Meta:
        verbose_name = 'Подтверждение email'
        verbose_name_plural = 'Подтверждения email'

    def __str__(self):
        return f'Подтверждение email для {self.user.email}'


