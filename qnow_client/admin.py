from django.contrib import admin
from .actions import remove_quotation, return_quotation
from .models import Quotation, MobilieType,QuotationStage
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.db.models import Value
from django.db.models.functions import Concat
import unidecode
from qnow_provider.models import QuotationPrice

# Classe que gera os campos mestre detalhe 
class QuotationPriceInline(admin.TabularInline):
    model = QuotationPrice
    extra = 0
    readonly_fields = ('quotation_number','quotation_provider','date_create','date_validate','quotation_value','delivery_time','form_payment','approved','approved_date','comments','commission_paid','commission_paid_date',)
    fields = ('quotation_number','quotation_provider','date_create','quotation_value','delivery_time','form_payment','approved','approved_date','comments',)
    ordering = ('quotation_value',)

# fields
# list_display
# list_filter
# search_fields
class MobileTypeAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    list_display = ('id','description',)
    search_fields = ('id','description')
    readonly_fields = ('id',)
    list_display_links = ('description',)


class QuotationStageAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    search_fields = ('status','description')
    readonly_fields = ('status','description',)
    list_display = ('id','status','description','explication')
   
class QuotationAdmin(admin.ModelAdmin):
    # Estudar seu uso
    #list_select_related = ('QuotationStage', 'MobileType')
    #preserve_filters = False
    #view_on_site = True


    # Executa uma ação quando em uma lista de dados
    actions = [remove_quotation,return_quotation]


    # Paginação para o listplay
    list_per_page = 50
    

    # Campos que aparecerão ao entrar na model
    list_display = ('id_quotation','client_client','get_number_launch','stage','date_create','date_update','date_validate','get_dif_date_now',
        'house_type','mobile_type_description','get_removed','phone_client','email_client','cep_client',
        'street_client','district_client','city_client','state_client','get_photo')

    # Campos que podem ser alterados na list_display diretamente
    list_editable  = ('stage',)

    # Campo ou campos específico para usar como link de acesso aos dados
    list_display_links = ('id_quotation','client_client',)

    # 1º Tipo 1 de pesquisa para tabelas relacionadas - Apresenta no modo lista e detalhado
    #raw_id_fields = ("stage","client")

    # 2º Tipo 2 de pesquisa para tabelas relacionadas - Apresenta no modo lista e detalhado
    autocomplete_fields = ("stage","client")
    

    # Sub-campos - Usado somente no list_display
    def mobile_type_description(self,Quotation):
        if str(Quotation.mobile_type).lower() == '_outro':
            return Quotation.mobile_description
        elif str(Quotation.mobile_type).lower() != '_outro' and str(Quotation.mobile_description) != '':            
            return str(Quotation.mobile_type)+str('*')+str(Quotation.mobile_description)+str('*')
        else:
            return Quotation.mobile_type
    mobile_type_description.short_description = 'Móvel'        

    def id_quotation(self, Quotation):
        return Quotation.id
    id_quotation.short_description = 'Número'        

    def client_client(self, Quotation):
        return Quotation.client
    client_client.short_description = 'Cliente'        

    def email_client(self, Quotation):
        return Quotation.client.email
    email_client.short_description = 'E-mail'       

    def cep_client(self, Quotation):
        return Quotation.client.cep
    cep_client.short_description = 'CEP'

    def street_client(self, Quotation):
        return Quotation.client.street
    street_client.short_description = 'Endereço'

    def district_client(self, Quotation):
        return Quotation.client.district
    district_client.short_description = 'Bairro'

    def city_client(self, Quotation):
        return Quotation.client.city
    city_client.short_description = 'Cidade'

    def state_client(self, Quotation):
        return Quotation.client.state
    state_client.short_description = 'Estado'

    def phone_client(self, Quotation):
        return Quotation.client.phone
    phone_client.short_description = 'Telefone'

    # Sub-campos para outros fins    
    def removed(self,Quotation):
        if Quotation.removed == True:
            return 'Sim'
        else:
            return 'Não'
    removed.short_description = 'Removida'

    # Campos que aparecerão ao entrar nos detalhes do model
    # Modo agrupado - Denomina um grupo de informações separada por um título
    fieldsets = (
        ('Dados do Cliente',{'fields': (('id','client','date_create','date_validate') )}),
        ('Dados da Cotação',{'fields': (('house_type','mobile_type'),'mobile_description','stage' )}),
        ('Fotos da Cotação',{'fields': ('image_environment','image_project')}),
        ('Detalhamento',    {'fields': ('particulars','removed')}),
    )

    # Apresenta em forma de radio campos de um relacionamento(foreignkey ou Choice)
    radio_fields = {"house_type": admin.VERTICAL}

    # Desativa a edição do campo, e com isto ele pode ser usado na tela de detalhes
    readonly_fields = ('id',)


    # Modo simples - Mosta as informações agrupando somente os campos por linha
    #fields = (('client','date_create'),('house_type','mobile_type'),('mobile_description','stage','removed'),'image_environment','image_project','particulars')    

    # Campos que unidos são usados no processo de filtragem por seleção
    list_filter = ('date_create','date_update','client__city','stage__description')


    # Campos que unidos são usados no processo de filtragem por digitação
    search_fields = ('id','client__username','mobile_type__description','client__email','client__street','stage__description','date_create','date_update','client__city')

    # Se true, aparece um campo para salvar e duplicar
    save_as = False

    # Este somente funciona se o de save_as = True. Não entendi bem o uso dele!
    save_as_continue = True

    # Duplica os botões de salvar, apagar e editar em cima 
    save_on_top = True

    # Força a informa o total de registros na tabela se false, mostra o texto "Mostrar Tudo"
    show_full_result_count = True

    # Mostra o conteudo da tabela relacionada
    inlines = (QuotationPriceInline,)

admin.site.register(MobilieType,MobileTypeAdmin)
admin.site.register(QuotationStage,QuotationStageAdmin)
admin.site.register(Quotation,QuotationAdmin)
