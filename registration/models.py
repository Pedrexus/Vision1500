from django.contrib.auth.models import User, AbstractUser
from django.db import models

from .validators import phone_regex


class MyUser(AbstractUser):
    full_name = models.CharField(max_length=50, verbose_name='Nome completo')
    email = models.EmailField(verbose_name='e-mail', unique=True)
    email_confirmed = models.BooleanField(default=False,
                                          verbose_name='e-mail verificado?')
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    verbose_name='Contato telefônico')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.full_name
