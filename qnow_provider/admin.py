from django.contrib import admin
from .models import QuotationPrice

# Register your models here.
class QuotationPriceAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    list_display = ('id','quotation_number_id','quotation_provider','date_create','date_validate','quotation_value','approved','delivery_time','form_payment')

    # 2º Tipo 2 de pesquisa para tabelas relacionadas - Apresenta no modo lista e detalhado
    autocomplete_fields = ("quotation_number",)

admin.site.register(QuotationPrice,QuotationPriceAdmin)