from django import template
from qnow_provider.models import QuotationPrice
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag(name='get_price_client_provider')
def get_price_client_provider(quotation_id,stage_number):
    '''
    Função que carrega para as cotações já orçada a lista de provider e seus valores
    Se uma cotação foi aprovada pelo client, somente esta será vistas
    '''
    # Stage = 4 indica cotação aprovada
    if stage_number == 4:
       quotationprice = QuotationPrice.objects.filter(quotation_number_id=quotation_id,approved=True).order_by('quotation_value')        
    else:    
       quotationprice = QuotationPrice.objects.filter(quotation_number_id=quotation_id).order_by('quotation_value')        
    return quotationprice

@register.simple_tag(name='get_price')
def get_price(instance,user_id):
    '''
    Função que retorna o lance dado por um provider a uma dita cotação
    Também análisa se a cotação esta aprovada, para somente trazer o valor a frente do provider correto
    '''
    try:
        if instance.stage.status == 4:
            qvalue = QuotationPrice.objects.get(quotation_number_id=instance.id,quotation_provider_id=user_id,approved=True)
        else:    
            qvalue = QuotationPrice.objects.get(quotation_number_id=instance.id,quotation_provider_id=user_id)
    except QuotationPrice.DoesNotExist:
        return 0
    return qvalue.quotation_value
    
@register.simple_tag(name='get_status')
def get_status(instance,user_id,status,number_launch, dif_day):
    '''
    Função que retorna informações da cotação perante seu status e nº lances efetuados pelo provider
    Pâramntros 
    Status:         É a situação da cotação  
    number_lanch:   Nº de lançamentos feito para uma cotação
    dif_day:        Nº de dias a espera e lance
    '''
    # Testando cotação cancelada pelo cliente
    if status == 5:
        return "Cotação CANCELADA pelo cliente!"
    # Testando cotação desativada pela plataforma    
    elif status == 6:
        return "Cotação DESATIVADA pela plataforma!"
    # Testando cotação a espera de lances    
    elif status == 2:
        # Quando ainda não houve lances para a dita cotação
        if number_launch == 0:
            if dif_day > 0:
                return "Este cliente esta à "+str(dif_day)+" dias aguardando sua resposta!"
            else:
                return "Cotação de hoje à espera de valor!"
        else:
            # Retorna o valor lançado na dita cotação pelo provider logado
            value_quotation = get_price(instance,user_id)

            if int(value_quotation) > 0:
                if number_launch > 1:
                    return  mark_safe("Seu orçamento R$ "+str(value_quotation)+" + "+'<label class="provider_list_number">%s</label>' % (str(number_launch)))
                else:    
                    return "Seu orçamento R$ "+str(value_quotation)
            else:
                if (number_launch) == 1:
                    return mark_safe('<label class="provider_list_number" style="background-color: red; border: 1px solid red;">%s</label>' % (str(number_launch))+" já orçou, falta você agora!")
                else:    
                    return mark_safe('<label class="provider_list_number" style="background-color: red; border: 1px solid red;">%s</label>' % (str(number_launch))+" já orçaram, falta você agora!")

    # Testando cotação orçada=3 
    elif status == 3:         
        # Retorna o valor lançado na dita cotação pelo provider logado
        value_quotation = get_price(instance,user_id)

        if int(value_quotation) > 0:
            if number_launch > 1:
                return  mark_safe("Seu orçamento R$ "+str(value_quotation)+" + "+'<label class="provider_list_number">%s</label>' % (str(number_launch)))
            else:    
                return "Seu orçamento R$ "+str(value_quotation)
        else:
            if (number_launch) == 1:
                return mark_safe('<label class="provider_list_number" style="background-color: red; border: 1px solid red;">%s</label>' % (str(number_launch))+" já orçou, falta você agora!")
            else:    
                return mark_safe('<label class="provider_list_number" style="background-color: red; border: 1px solid red;">%s</label>' % (str(number_launch))+" já orçaram, falta você agora!")

    # Testando cotação aprovada=4
    elif status == 4:         
        # Retorna o valor lançado na dita cotação pelo provider logado
        value_quotation = get_price(instance,user_id)

        if int(value_quotation) > 0:
            return mark_safe('<label class="provider_list_number" style="background-color: #FFB400; border: 1px solid #FFB400;">%s</label>' % ('A')+"Aprovado! Você R$ "+str(value_quotation))                            
        else:    
            if instance.stage.status == 4:
                return mark_safe('<label class="provider_list_number" style="background-color: red; border: 1px solid red;">%s</label>' % ('x')+" Aprovado! Outro fornecedor")                
            else:    
                return "Aprovado mas sem valor!"
