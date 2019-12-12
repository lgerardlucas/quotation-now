import re
from django.db import models
#from django.contrib.localflavor.br.forms import BRStateSelect
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)

class User(AbstractBaseUser, PermissionsMixin):

    #username = models.CharField('Usuário', max_length=100,unique=True)
        #, unique=True, 
        #validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
        #    'O nome de usuário só pode conter letras, digitos ou os '
        #    'seguintes caracteres: @/./+/-/_', 'invalid')])

    email = models.EmailField('E-mail', unique=True)
    username = models.CharField('Nome e Sobrenome', unique=True, max_length=100, blank=False)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    role = models.CharField('Classificação', max_length=10, blank=True, default='Indefinido')
    phone = models.CharField('Telefone', max_length=50, blank=False)
    cep = models.CharField('Cep', max_length=9, blank=False)
    street = models.CharField('Rua', max_length=200, blank=False, default='Indefinido')
    district = models.CharField('Bairro', max_length=50, blank=False, default='Indefinido')
    city = models.CharField('Cidade', max_length=50, blank=False, default='Indefinido')
    state = models.CharField('Estado', max_length=50, blank=False, default='Indefinido')

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_short_username(self):
        return self.username

    def get_full_username(self):
        return str(self)

    class Meta:
        app_label = 'qnow_user'
        db_table = 'qnow_user_user'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'