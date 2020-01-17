from django.shortcuts import render, redirect, Http404, render_to_response, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
import threading
import datetime
from django.contrib import messages
from qnow_client.models import Quotation, QuotationStage
from .forms import QuotationPriceForm
from .models import QuotationPrice
from qnow_user.models import User
from django.db.models import Q
from qnow_site.utils import convert_date_to_br

# Lista as cotações de todos os clients com status = 2(Liberado para orçar)
@login_required
def quotation_provider(request):
    template_name = "../templates/provider_quotation_list.html"

    # Verifica o acesso do cliente na opção provider, força a entrar corretamente
    if request.user.role == 'client':
        # Messagem de alerta, onde o cliente usa o acesso errado a plataforma
        messages.add_message(request, messages.INFO, 'Desculpe, acesso restrito a marcenarias!')
        messages.add_message(request, messages.INFO, 'Tente novamente aqui e agora.')

        # Executa logout quanto fora da área de cotação
        logout(request)

        settings.LOGIN_REDIRECT_URL = 'qnow_client:quotation_client'
        return redirect('qnow_user:login_client')

    # GET - Status da cotação a ser pesquisado
    queryset_stage = request.GET.get('stage_list')

    # GET - Cidade ser pesquisado as cotações
    queryset_city = request.GET.get('city_list')
    # Sub-campos: Retorna o valor de cada cotação referente ao provider 
    def get_price_provider(self):
        if self.quotation_provider == User.id:
            return 1
        else:
            return 2
    get_price_provider = 'Valor'     

    # GET - Por diversos campos
    queryset = request.GET.get('q')
    if queryset or queryset_stage or queryset_city:
        # -1 = Todos ou X para individual
        if queryset_stage == '-1':
            stage_list_start = 2
            stage_list_stop  = 6
        else:
            stage_list_start = queryset_stage
            stage_list_stop  = queryset_stage

        if not queryset_city:
            queryset_city = ''

        # Pesquisa via Like + Or
        quotations = Quotation.objects.filter(
            Q(id__icontains=queryset)|
            Q(client__username__icontains=queryset)|
            Q(date_create__icontains=queryset)|            
            Q(house_type__icontains=queryset)|
            Q(house_set__icontains=queryset)|  
            Q(mobile_type__description__icontains=queryset)|
            Q(mobile_description__icontains=queryset)).filter(
            Q(client__city__icontains=queryset_city)
            ).filter(stage_id__status__range=[stage_list_start,stage_list_stop],removed=False).order_by('client__city','id')

    else:
        # GET - Status da cotação a ser pesquisado
        queryset_stage = '-1'
        
        # GET - Cidade ser pesquisado as cotações
        queryset_city = ''

        # Pesquisa as cotações com status = 2 a 6 
        quotations = Quotation.objects.filter(stage_id__status__range=[2,6],removed=False).order_by('client__city','id')
    
    # Lista dos status liberados para uso na tag SELECT
    quotationsstages = QuotationStage.objects.filter(status__range=[2,6]).order_by('status')

    # Lista das cidades liberados para uso na tag SELECT
    quotationscitys = User.objects.filter().order_by('city').distinct('city')

    # Lambda que retorna a quantidade de dados para ser listados
    if quotations.count() > 0:
        message = ''
    else:
        message = 'Nenhuma cotação encontra!'

    # Verifica se encontrou e renderiza
    if Quotation.id:
        context = { "active_page_client_provider": "active", 
                    "message": message,
                    "provider_email": request.user.email,
                    "quotationstage_select":str(queryset_stage),
                    "quotationcity_select":queryset_city,
                    "quotations": quotations,
                    "quotationsstages": quotationsstages,
                    "quotationscitys": quotationscitys
                }
        return render(request, template_name, context)

# Mostra os detalhes e caracteristicas de uma cotação específica
@login_required
def quotation_provider_detail(request,quotation_id=0):
    template_name = "../templates/provider_quotation_detail.html"


    # Pesquisa pelo seu id
    quotation = Quotation.objects.filter(pk=quotation_id,removed=False)

    # Lambda que retorna a quantidade de dados para ser listados
    if quotation.count() > 0:
        message = ''
    else:
        message = str(request.user) + ', Nenhuma cotação disponível para cotação!'

    # Verifica se encontrou e renderiza
    if Quotation.id:
        context = { "active_page_client_provider": "active", 
                    "message": message,
                    "quotation": quotation}
        return render(request, template_name, context)


# Mostra alguns detalhes com fotos menores e campos para cotar
@login_required
def quotation_provider_price(request,quotation_id=0):
    template_name = "../templates/provider_quotation_price.html"

    # GET - Retorna dados cotação com um todo
    quotation = Quotation.objects.filter(pk=quotation_id,removed=False)
    form = QuotationPriceForm(request.POST or None, initial={'quotation_number':quotation_id,'quotation_provider':request.user,'date_create':convert_date_to_br(quotation[0].date_create)})

    # GET - Verifica se a cotação tem orçamento
    quotationprice = QuotationPrice.objects.filter(quotation_number_id=quotation_id,quotation_provider=request.user)        
    # Se tiver orçamento, retorna queryset com os dados e monta o form
    if quotationprice:
        quotationprice = QuotationPrice.objects.get(quotation_number_id=quotation_id,quotation_provider=request.user)        
        form = QuotationPriceForm(instance=quotationprice)

    # Enviando o context para o template
    context = { "active_page_client_provider": "active", 
                "quotation": quotation,
                "quotationprice":form
            }
    return render(request, template_name, context)


# Grava o valor orçado pelo provider logado 
@login_required
def quotation_provider_price_post(request,quotation_id=0):
    template_name = "../templates/provider_quotation_price.html"
    if request.method == "POST":
        
        form = QuotationPriceForm(request.POST or None)
        if form.is_valid():     
            post = form.save(commit=False)
            try:
                # Retorna o stage(estágio)-Quando houver um lance mudamos o stage para 3 orçado
                quotationstage  = QuotationStage.objects.get(status=3)

                # GET - Retorna dados cotação com um todo
                quotation = Quotation.objects.get(pk=quotation_id,removed=False)

                # Altera para o stage = 3 orçado
                if quotation.stage_id != quotationstage.id:
                    quotation.stage_id  = quotationstage.id
                    quotation.save()

                # Após salvar, enviar um email ao cliente/fornecedor e uma mensagem na tela
                messages.add_message(request, messages.INFO, 'Cotação Nº: '+str(quotation.id)+' orçada com sucesso!')

                t1 = threading.Thread(target=quotation_provider_email, args=(
                    quotation,                      # Dados dos cliente
                    post.quotation_value,           # Valor orçado pelo provider
                    request.user.username,          # Usuário logado(provider)
                    'orçada',                       # Situação para troca no banco
                    settings.SEND_EMAIL_SIS,        # Regra para envio de email
                    str(post.date_validate),        # Data de validade do valor orçado
                    post.delivery_time,             # Data de validade do valor orçado
                    post.form_payment,              # Forma de pagamento
                    post.comments                   # Comentário do provider
                    )
                )
                t1.start()


                if settings.SEND_EMAIL_SIS == True:
                    messages.add_message(request, messages.SUCCESS, 'Um e-mail de confirmação foi enviado pra você e ao cliente.')

            except Quotation.DoesNotExist:
                # Após salvar, enviar um email ao cliente e a marcenaria uma mensagem na tela
                messages.add_message(request, messages.INFO, 'Erro na Cotação Nº: '+str(quotation.id)+'! volte para lista de cotações e tente novamente.')
                return  redirect("qnow_provider:quotation_provider_detail",quotation_id)

            post.save()
        else:
            post = form.save(commit=False)
            # GET - Retorna dados cotação com um todo
            quotation = Quotation.objects.filter(pk=quotation_id,removed=False)
            
            # Enviando o context para o template
            context = { "active_page_client_provider": "active", 
                "quotation": quotation,
                "quotationprice":form
            }
            # Se ocorrer erro de validação dos dados, montar 
            return render(request, template_name, context)

        # Se incluido corretamnte, voltar a tela de detalhe    
        return redirect("qnow_provider:quotation_provider_detail",quotation_id)


#Envia um e-mail ao cliente e para MGA-Cotações como valor orçado pelo provider 
def quotation_provider_email(request,value=0.00,provider_name='',acao='ERROR',send_email_sis='False',date_validate='',deliver_time='',form_payment='',commets=''):
    if send_email_sis == True:
        template_name = "../templates/provider_email.html"
        
        subject = 'MGA-Cotações - Cotação Nº: '+str(request.id)+' - '+str(request.client)
        message = 'Parabéns, sua cotação foi '+acao+' com sucesso!'
            
        from_email = settings.EMAIL_HOST_USER

        context = {
            "request":          request,
            "message":          message,
            "value":            value,
            "provider_name":    provider_name,
            "date_validate":    date_validate,
            "deliver_time":     deliver_time,
            "form_payment":     form_payment,
            "commets":          commets,
            "message_alert":'Este e-mail alerta você, de que uma marcenaria lançou um valor para sua cotação. Se o valor estiver dentro do esperado, poderá acessar a plataforma e aprová-lo ou esperar mais uns dias, a fim de que, outras marcenarias deem seus lances.',
            "message_aprovacao":'   Ao aprovar uma cotação, o cliente esta aprovando a marcenaria, para que a mesma, possa entrar em contato, finalizar os detalhes e tirar dúvidas, e com isto, realmente fechar o custo final de sua cotação. A MGA-Cotações, une cliente e marcenaria para que juntos produzam sonhos!'
            }
        content = render_to_string(template_name, context)
        if subject and message and from_email:
            try:
                email = EmailMessage(
                    subject,
                    content,
                    from_email, 
                    [request.client.email],
                    [from_email]
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Problema no envio do e-mail. Tente mais tarde!')
            return redirect("qnow_provider:quotation_provider")
        else:
            return redirect("qnow_provider:quotation_provider")


#Envia uma pergunta ao cliente via provider
def quotation_provider_email_inquire(request,quotation_id=0):
    template_name = "../templates/provider_email_inquire.html"

    quotation = Quotation.objects.get(pk=quotation_id,removed=False)
    subject = 'MGA-Cotações - Cotação Nº: '+str(quotation_id)+' - '+str(quotation.client)
    message = 'Atenção, sua cotação contém uma dúvida.'
        
    from_email = settings.EMAIL_HOST_USER
    context = {
        "request":          quotation,                          # Quotação do cliente
        "message":          message,                            # Messagem de alerta
        "provider_name":    request.user.username,              # Nome do provider logado
        "inquire":          request.POST.get('inquire_provider')# Dúvida do provider
        }
    content = render_to_string(template_name, context)
    if subject and message and from_email:
        try:
            email = EmailMessage(
                subject,
                content,
                from_email, 
                [request.POST.get('email_client')],
                [from_email]
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Problema no envio do e-mail. Tente mais tarde!')
        return redirect("qnow_provider:quotation_provider")
    else:
        return redirect("qnow_provider:quotation_provider")
    
