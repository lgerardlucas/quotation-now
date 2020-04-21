from django.db import models
from cloudinary.models import CloudinaryField
from qnow_user.models import User
from qnow_provider.models import QuotationPrice
from django.conf import settings
from datetime import datetime,date,timedelta
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
import threading

User = get_user_model()

app_name = 'qnow_client'


# Define o caminho e a formatação das imagens
def user_directory_path(instance, filename):
    return "%s.%s" %(instance.slug, filename)
#    return "%s.%s.%s" %(datetime.now(), instance.slug, filename)


# Valida o tipo de arquivo válido
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.jpg','.png','.jpeg','.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Extensão não suportada!')

# Tabela com a lista de móveis
class MobilieType(models.Model):
    description = models.CharField(max_length=50,blank=False,unique=True)

    class Meta:
        verbose_name = 'Tipo de Móvel'
        verbose_name_plural = 'Tipo de Móveis'
        ordering = ["description"]

    def __str__(self):
        return self.description

# Tabela com os estágios da cotação
class QuotationStage(models.Model):
    status = models.IntegerField(blank=False,null=False,unique=True)    
    description = models.CharField('Situação',max_length=50,blank=False,unique=True)
    explication = models.CharField('Descrição da Situação',max_length=200,blank=False,unique=False,default="Aguardando texto...")

    class Meta:
        verbose_name = 'Estágio da Cotação'
        verbose_name_plural = 'Estágios da Cotação'
        ordering = ["status"]

    def __str__(self):
        return self.description


class Quotation(models.Model):
    # Nª da cotação e Id da tabela
    id = models.AutoField(primary_key=True)

    # Cliente da cotação
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default=User, related_name='quotation')   
    
    # Data de criação da cotação
    date_create = models.DateField('Emissão',default=date.today)


    # Data de validade da cotação
    date_validate = models.DateField('Validade(Data)',blank=False,null=False,default=datetime.now()+timedelta(days=15))


    # Data da última atualização da cotação
    date_update = models.DateField('Atualização',auto_now=True)
        
    # Tipo da residencia do cliente
    HOUSETYPECHOICES = (
    ('Apartamento', 'Apartamento'),
    ('Casa', 'Casa'),
    ('Comercial', 'Comercial'),
    ('Escritório', 'Escritório'),
    ('Outro', 'Outro'),
    )
    house_type = models.CharField('Tipo Imóvel',max_length=20,
        choices=HOUSETYPECHOICES,blank=False,default='Casa')
        
    # Estágio em que se apresenta a cotação
    stage = models.ForeignKey(QuotationStage,null=True,on_delete=True,related_name='QuotationStage', verbose_name='Estágio')

    # Define o tipo do local do imóvel                
    house_set = models.CharField(max_length=100,null=True,blank=True)

    # Definição do móvel
    mobile_type = models.ForeignKey(MobilieType,on_delete=True,related_name='MobileType',verbose_name='Móvel')

    # Definição manual do móvel quando não esta na lista acima
    mobile_description = models.CharField('Móvel Complementar',max_length=100,blank=True)

    # Descrição detalhada do móvel
    particulars  = models.TextField('Detalhes', blank=False)

    # Imagem do ambiente do móvel 
    image_environment = CloudinaryField('Imagem-1',null=True, blank=True)

    # Imagem do projeto
    image_project = CloudinaryField('Imagem-2',null=True, blank=True)
        
    slug = models.SlugField(max_length=150,unique=True)

    # Determina se a cotação foi removida
    removed = models.BooleanField('Removida',default=False)

    # Comentário do cliente feito depois da entrega
    comment  = models.TextField('Detalhes', blank=True)

    # Sub-campo: Indica o número de lances para uma dita cotação
    def get_number_launch(self):
        qvalue = QuotationPrice.objects.filter(quotation_number_id=self.id)
        return qvalue.count()
    get_number_launch.short_description = 'Orçtos'  


    # Sub-campo: Retorna a marcenaria vencedora quando o status for aprovado
    def get_provider_approved(self):
        quotation_price = QuotationPrice.objects.get(quotation_number=self.id,approved=True)  
        if not quotation_price:
            return "-"
        else:    
            return ' R$: '+str(quotation_price.quotation_value)+' '+str(quotation_price.quotation_provider)
    get_provider_approved.short_description = 'Dados da Aprovação'  


    # Sub-campo: Indica a existencia de foto em um dos campos
    def get_photo(self):
        if self.image_environment or self.image_project:
            return 'Sim'
        else:
            return 'Não'
    get_photo.short_description = 'Fotos'     
           
    # Sub-campo: Indica a remoação da cotação
    def get_removed(self):
        if self.removed:
            return 'Sim'
        else:
            return 'Não'
    get_removed.short_description = 'Removida'


    # Sub-campo: Indica a diferença entre a data de validade x data atual
    def get_dif_date_now(self):
        date1 = datetime.now().toordinal()
        date2 = self.date_validate.toordinal()
        return date1 - date2
    get_dif_date_now.short_description = 'Validade(Dias)'  

    class Meta:
        verbose_name = 'Cotação'
        verbose_name_plural = 'Cotações'
        ordering = ["-id"]

    def __str__(self):
        return str(self.client)

# Signals = Quando pelo admin a cotação for liberada para receber valor, 
# enviar email a todos os providers e ao cliente, comunicando dos fatos
@receiver(post_save, sender=Quotation)
def post_solicitacoes_save(sender, instance, **kwargs):
    if instance.stage.id == 27:
        from .views import quotation_client_email
        # E-mail enviado ao client
        t1 = threading.Thread(target=quotation_client_email, args=(instance,'liberada',settings.SEND_EMAIL_SIS))
        t1.start()

        # E-mail enviado aos provider 
        t1 = threading.Thread(target=quotation_client_email, args=(instance,'à espera',settings.SEND_EMAIL_SIS))
        t1.start()

