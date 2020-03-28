import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)
from datetime import datetime


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('E-mail', unique=True)
    username = models.CharField('Nome', unique=True, max_length=100, blank=False)
    is_active = models.BooleanField('Acessar o Sistema(S/N)', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    role = models.CharField('Classificação', max_length=10, blank=True, default='Indefinido')
    phone = models.CharField('Telefone', max_length=50, blank=False)
    cep = models.CharField('Cep', max_length=9, blank=False)
    street = models.CharField('Endereço', max_length=200, blank=False, default='Indefinido')
    district = models.CharField('Bairro', max_length=50, blank=False, default='Indefinido')
    city = models.CharField('Cidade', max_length=50, blank=False, default='Indefinido')
    state = models.CharField('Estado', max_length=50, blank=False, default='Indefinido')

    # Quando definido True, o usuário NÃO PODERÁ interagir/receber emails com o sistema todo(cotações e lances)
    approved = models.BooleanField('Desativar Movimentação', blank=True, default=False)

    contract_accepted = models.BooleanField('Li e concordo(S/N)', blank=True, default=False)
    contract_date_accepted = models.DateTimeField('Li e concordei em:',default=datetime.now)

    # Data de nascimento para client e para a empresa do provider
    birth_date      = models.DateField('Data de Inicio das Atividades',blank=True, null=True)

    # Prazo de entrega para provider
    delivery_time       = models.CharField('Prazo de Entrega Padrão',max_length=30,null=True,blank=True)

    # Forma de pagamento para provider 
    form_payment        = models.CharField('Forma de Pagamento Padrão',max_length=50,null=True,blank=True)

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_short_username(self):
        return self.username

    def get_full_username(self):
        return str(self)
    
    '''
    # Sub-campo: que retorna a qtde de cotações em diversos stages - PENDENTE
    def get_number_launch_client_pendente(self):
        from qnow_client.models import Quotation,QuotationStage
        qnumber = Quotation.objects.filter(client=self.id,client__role='client',stage_id=QuotationStage.objects.get(status=0).id)
        if qnumber:
            return qnumber.count()
        else:    
            return '--'
    get_number_launch_client_pendente.short_description = "P"     
    
    # Sub-campo: que retorna a qtde de cotações em diversos stages - EM ANALISE
    def get_number_launch_client_analise(self):
        from qnow_client.models import Quotation,QuotationStage
        qnumber = Quotation.objects.filter(client=self.id,client__role='client',stage_id=QuotationStage.objects.get(status=1).id)
        if qnumber:
            return qnumber.count()
        else:    
            return '--'
    get_number_launch_client_analise.short_description = "E"     
    '''

    # Sub-campo: que retorna a qtde de cotações em diversos stages - LIBERADO
    def get_number_launch_client_liberado(self):
        from qnow_client.models import Quotation,QuotationStage
        qnumber = Quotation.objects.filter(client=self.id,client__role='client',stage_id=QuotationStage.objects.get(status=2).id)
        if qnumber:
            return qnumber.count()
        else:    
            return '--'
    get_number_launch_client_liberado.short_description = "L"     

    # Sub-campo: que retorna a qtde de cotações em diversos stages - ORÇADO
    def get_number_launch_client_orcado(self):
        from qnow_client.models import Quotation,QuotationStage
        qnumber = Quotation.objects.filter(client=self.id,client__role='client',stage_id=QuotationStage.objects.get(status=3).id)
        if qnumber:
            return qnumber.count()
        else:    
            return '--'
    get_number_launch_client_orcado.short_description = "O"     

    # Sub-campo: que retorna a qtde de cotações em diversos stages - APROVADO
    def get_number_launch_client_aprovado(self):
        from qnow_client.models import Quotation,QuotationStage
        qnumber = Quotation.objects.filter(client=self.id,client__role='client',stage_id=QuotationStage.objects.get(status=4).id)
        if qnumber:
            return qnumber.count()
        else:    
            return '--'
    get_number_launch_client_aprovado.short_description = "A"     
    
    class Meta:
        app_label = 'qnow_user'
        db_table = 'qnow_user_user'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
