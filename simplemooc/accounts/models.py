import re

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.core import validators
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Nome de usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(
            re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, dígitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid'
        )]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome completo', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)


class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets', on_delete=models.CASCADE
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} em {self.created_at}'

    def key_has_expired(self):
        days_from_creation = (timezone.now() - self.created_at).days
        return days_from_creation > settings.PASSWORD_RESET_TIMEOUT_DAYS

    def confirm(self):
        self.confirmed = True
        self.save()
