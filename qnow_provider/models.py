from django.db import models
from datetime import datetime,date,timedelta
from qnow_user.models import User
from django.core import validators

def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s não é um inteiro ou moeda válido!'),
            params={'value': value},
        )
        
class QuotationPrice(models.Model):
    # ID da tabela e Nº da cotação
    quotation_number    = models.ForeignKey('qnow_client.Quotation',on_delete=True,related_name='quotation_price',verbose_name='Cliente')

    # ID do provider 
    quotation_provider  = models.ForeignKey("qnow_user.User", on_delete=models.CASCADE, null=True,related_name="quotation_provider",verbose_name='Marcenaria') 

    # Data do lançamento do preço
    date_create         = models.DateField('Data da Orçamento',default=date.today)

    # Data de validade do preço
    date_validate       = models.DateField('Validade da Cotação',blank=False,null=False,default=datetime.now()+timedelta(days=10))

    # Valor da cotação
    quotation_value     = models.DecimalField('Valor da Cotação',max_digits=8, decimal_places=2)

    # Prazo de entrega
    delivery_time       = models.CharField('Prazo de Entrega',max_length=30,null=False,blank=False,default='')

    # Forma de pagamento
    form_payment        = models.CharField('Forma de Pagamento',max_length=50,null=False,blank=False,default='')

    # Quotation aprovada pelo client
    approved            = models.BooleanField('Aprovado?',default=False)

    # Informações a mais para o cliente
    comments            = models.TextField('Comentário da Marcenaria',blank=True)

     # Sub-campo: Indica a diferença entre a data de criação x data atual
    def get_dif_date_validate(self):
        date1 = datetime.now().toordinal()
        date2 = self.date_validate.toordinal()
        return date1 - date2
    get_dif_date_validate.short_description = 'Validade(Dias)'  

     # Sub-campo: Indica o valor quando aprovado a receber do provider
    def get_value_percent_site(self):
        if self.approved:
            qvalue_approved = self.quotation_value * 5 / 100
            return "% 12.2f" % qvalue_approved
        else:
            return "--"    
    get_value_percent_site.short_description = 'Monetização'  

    class Meta():
        verbose_name = 'Preço'
        verbose_name_plural = 'Preços'
        ordering = ["quotation_number"]
        unique_together = (('quotation_number','quotation_provider'),)
