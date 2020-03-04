from django.contrib import admin
from .models import QuotationPrice
from qnow_client.models import Quotation

# Register your models here.
class QuotationPriceAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    list_display = ('id','number_quotation','quotation_client','quotation_provider','value_quotation','approved','date_create','date_validate','delivery_time','form_payment')

    # 2º Tipo 2 de pesquisa para tabelas relacionadas - Apresenta no modo lista e detalhado
    autocomplete_fields = ("quotation_number",)

    # Paginação para o listplay
    list_per_page = 30

    # Campos que unidos são usados no processo de filtragem por seleção
    list_filter = ('quotation_number_id','quotation_provider','approved')

    # Sub-campos - Usado somente no list_display
    #Retorna o nome do cliente da cotação por meio do relacionamento na models QuotationPrice
    def quotation_client(self, QuotationPrice):
        return QuotationPrice.quotation_number
    quotation_client.short_description = 'Cliente da cotação'        

    def number_quotation(self, QuotationPrice):
        return QuotationPrice.quotation_number.id
    number_quotation.short_description = 'Nº Cotação'        

    def value_quotation(self, QuotationPrice):
        return QuotationPrice.quotation_value
    value_quotation.short_description = 'Valor Orçado'        


    # Campos que unidos são usados no processo de filtragem por digitação
    search_fields = ('date_create','date_validate','quotation_value','approved','delivery_time','form_payment')

admin.site.register(QuotationPrice,QuotationPriceAdmin) 