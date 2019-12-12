from django.contrib import admin
from .models import Contact
from .actions import check_email_contact, uncheck_email_contact,check_email_contact_whith_return
from django.urls import reverse

class ContactAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    list_display = ('name','date_send','email_send','subject_send',
        'return_send','email_with_answer','date_update')

    # Verifica se o e-mail tem resposta digitada
    def email_with_answer(self,Contact):
        if Contact.message_return:
            returned = "Sim"
        else:
            returned = "Não"

        return returned
    email_with_answer.short_description = 'E-mail com resposta?'        


    # Paginação para o listplay
    list_per_page = 15

    # Desativa a edição do campo, e com isto ele pode ser usado na tela de detalhes
    readonly_fields = ('name','date_send','email_send','subject_send','copy_send',)

    # Executa uma ação quando em uma lista de dados
    actions = [check_email_contact,check_email_contact_whith_return,uncheck_email_contact]

    # Campos que aparecerão ao entrar nos detalhes do model
    # Modo agrupado - Denomina um grupo de informações separada por um título
    fieldsets = (
        ('Dados do Remetente',{'fields': ('name','date_send','email_send',)}),
        ('Assunto',{'fields': ('subject_send', )}),
        ('Situação do E-mail',{'fields': ('return_send',)}),
        ('Mensagem',{'fields': ('message_send','message_return')}),
    )

admin.site.register(Contact,ContactAdmin)