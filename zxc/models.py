from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # Переопределяем стандартные поля, если нужно
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True)

    # Дополнительные поля
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    address = models.TextField(_('address'), blank=True)

    # Настройки модели
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name() or self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user')
    )

    # Дополнительные поля профиля
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        null=True,
        blank=True
    )
    bio = models.TextField(_('about me'), blank=True)
    email_verified = models.BooleanField(_('email verified'), default=False)

    # Настройки спортивных предпочтений
    preferred_sports = models.CharField(
        _('preferred sports'),
        max_length=255,
        blank=True,
        help_text=_('Comma-separated list of preferred sports')
    )

    # Статистика
    rentals_count = models.PositiveIntegerField(_('rentals count'), default=0)
    last_activity = models.DateTimeField(_('last activity'), auto_now=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


class EmailVerification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_verifications',
        verbose_name=_('user')
    )
    email = models.EmailField(_('email address'))
    token = models.CharField(_('token'), max_length=64, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('expires at'))
    is_verified = models.BooleanField(_('is verified'), default=False)

    class Meta:
        verbose_name = _('email verification')
        verbose_name_plural = _('email verifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification for {self.email}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name=_('user')
    )
    token = models.CharField(_('token'), max_length=64, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('expires at'))
    is_used = models.BooleanField(_('is used'), default=False)

    class Meta:
        verbose_name = _('password reset token')
        verbose_name_plural = _('password reset tokens')
        ordering = ['-created_at']

    def __str__(self):
        return f"Password reset for {self.user.email}"



AUTH_USER_MODEL = 'accounts.User'  # предполагается, что модели в приложении accounts


