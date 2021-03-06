from django.shortcuts import render, redirect, Http404, render_to_response, get_list_or_404, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.utils.safestring import mark_safe
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime,date,timedelta
from django.core.mail import EmailMessage, BadHeaderError, EmailMultiAlternatives
from django.conf import settings
import uuid
import threading
from .models import Quotation, QuotationStage
from qnow_provider.models import QuotationPrice
from .forms import QuotationForm
from qnow_user.models import User

# Função lambda que retorna um count de Quotation chamada pela def quotation_client
count_quotation = lambda client : Quotation.objects.filter(client_id=client).count()

# Função para o erro 404 - Somente com DEBUG = False 
def error_404_view(request, exception):
    Context = {"message": "Quando uma página não é encontrada, indica que algo deu errado ou que o endereço informado esta incorreto!"}
    return render(request,'../qnow_site/templates/404.html', Context)

# Função para o erro 500 - Somente com DEBUG = False 
def error_500_view(request):
    Context = {"message": "Erro 500 - Desculpe pelo erro!"}
    return render(request,'../qnow_site/templates/500.html', Context)


# Grava a cotação do cliente
@login_required
def quotation_client(request):
    template_name = "../templates/client_quotation.html"

    # Verifica o acesso do provider na opção cliente, força a entrar corretamente
    if request.user.role == 'provider':
        # Messagem de alerta, onde o provider usa o acesso errado a plataforma
        messages.add_message(request, messages.INFO, 'Desculpe, acesso restrito aos clientes!')
        messages.add_message(request, messages.INFO, 'Tente novamente aqui e agora.')

        # Executa logout quanto fora da área de cotação
        logout(request)

        settings.LOGIN_REDIRECT_URL = 'qnow_provider:quotation_provider'
        return redirect('qnow_user:login_provider')

    form = QuotationForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if request.user.is_authenticated:
            Quotation = form.save(commit=False)

            # Retorna o stage(estágio) padrão para inclusão 0 = Pendente
            quotationstage = QuotationStage.objects.get(status=0)
            Quotation.stage_id = quotationstage.id

            # Gravando o usuário logado a cotação
            Quotation.client = request.user

            # UUID gerado para o campo slug
            if not Quotation.id:
                Quotation.slug = uuid.uuid4()

            # Gravando e redirecionando para a lista de cotações do usuário
            if form.is_valid():
                form.save(commit=True)

                # Após salvar, enviar um email ao cliente e uma mensagem na tela
                messages.add_message(request, messages.SUCCESS, 'Cotação Nº: '+str(Quotation.id)+' envida com sucesso!')

                t1 = threading.Thread(target=quotation_client_email, args=(Quotation,'cadastrada',settings.SEND_EMAIL_SIS))
                t1.start()
                #quotation_client_email(Quotation,'cadastrada',settings.SEND_EMAIL_SIS)
                if settings.SEND_EMAIL_SIS == True:
                    messages.add_message(request, messages.SUCCESS, 'Um e-mail de confirmação foi enviado pra você. Verifique sua conta de e-mail.')

                return redirect("qnow_client:quotation_client_list", Quotation.client_id)
            else:
                form = QuotationForm()
        else:
            # Se não estiver conectado, redirecionar para tela de login
            context = {"origin": "client", "active_page_client_provider": "active"}
            return redirect("qnow_user:login_client_start")
    else:
        form = QuotationForm()
       
    context = {"active_page_client_provider": "active", "acao": "Enviar", "form": form}
    return render(request, template_name, context)


# Lista as cotações do cliente logado
@login_required #(redirect_field_name='qnow_user:login_provider_start')
def quotation_client_list(request, client_id=0):
    template_name = "../templates/client_quotation_list.html"

    # Verifica se o usuário logado é o mesmo requisitado
    if client_id != request.user.id:
        response = render_to_response('404.html')
        response.status_code = 404
        return response

    # Pesquisa as cotações do usuário logago
    quotation = Quotation.objects.filter(client=client_id,removed=False)

    # Lambda que retorna a quantidade de dados para ser listados
    if quotation.count() > 0:
        message = ''
    else:
        message = str(request.user) + ', você ainda não possui cotações!'


    # Verifica se encontrou e renderiza
    if Quotation.id:
        context = { "active_page_client_provider": "active", 
                    "message": message,
                    "quotation": quotation}
        return render(request, template_name, context)

# Marca qual cotação foi aprovada pelo cliente e envia um email para os interessados
@login_required
def quotation_client_approved(request,quotationprice_id=0):
    if request.POST.get('price_id'):
        # Reprova todos os orçamentos primieiro. Isto garante a aprovação correta quando o client resolver trocar de provider
        QuotationPrice.objects.filter(quotation_number=quotationprice_id).update(approved=False)  

        # Aprova o valor orçado pelo provider 
        quotationprice_update_row = QuotationPrice.objects.filter(pk=request.POST.get('price_id')).update(approved=True,commission_paid_date=datetime.now()+timedelta(days=7),approved_date=datetime.now())  

        # Retorna id para o stage = 4 aprovado
        quotationstage = QuotationStage.objects.get(status=4)

        # Alterando o stage da cotação para 4 = aprovado 
        Quotation.objects.filter(pk=quotationprice_id).update(stage_id=quotationstage.id)

        # Após aprovar, enviar um email ao cliente e a marcenaria e uma mensagem na tela
        messages.add_message(request, messages.INFO, 'Cotação Nº: '+str(quotationprice_id)+' aprovada com sucesso!')

        # Dados para o envio do email

        quotation_email =  Quotation.objects.get(pk=quotationprice_id)

        t4 = threading.Thread(target=quotation_client_email, args=(quotation_email,'aprovada',settings.SEND_EMAIL_SIS))
        t4.start()

        if settings.SEND_EMAIL_SIS == True:
            messages.add_message(request, messages.INFO, 'Verifique sua conta de e-mail.')

    else:
        # 
        messages.add_message(request, messages.INFO, 'Atenção! Para aprovar uma cotação, é preciso marcá-la!')
        messages.add_message(request, messages.INFO, 'Volte a cotação Nº: '+str(quotationprice_id)+' e marque-a!')

    # Incluir melhores testes aqui
    return redirect("qnow_client:quotation_client_list", request.user.id)

@login_required
def quotation_client_edit(request, quotation_id=0):
    template_name = "../templates/client_quotation.html"

    # Localiza a cotação pelo seu id para edição
    quotation = get_object_or_404(Quotation, pk=quotation_id)

    # Verifica se o usuário logado é o mesmo requisitado
    if quotation.client_id != request.user.id:
        raise Http404

    form = QuotationForm(instance=quotation)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = QuotationForm(
                request.POST or None, request.FILES or None, instance=quotation
            )
            if form.is_valid():
                form.save()
     
                # Após salvar, enviar um email ao cliente e uma mensagem na tela
                messages.add_message(request, messages.INFO, 'Cotação Nº: '+str(quotation.id)+' alterada com sucesso!')

                t2 = threading.Thread(target=quotation_client_email, args=(quotation,'alterada',settings.SEND_EMAIL_SIS))
                t2.start()
                #quotation_client_email(quotation,'alterada',settings.SEND_EMAIL_SIS)
                if settings.SEND_EMAIL_SIS == True:
                    messages.add_message(request, messages.INFO, 'Verifique sua conta de e-mail.')

                # Depois de salvo, renderizar pra lista de cotações do usúario
                return redirect("qnow_client:quotation_client_list", quotation.client_id)
        else:
            context = {"origin": "client", "active_page_client_provider": "active"}
            return redirect("qnow_user:login_client_start")
    else:
        context = {
            "active_page_client_provider": "active",
            "acao": "Enviar",
            "form": form,
        }
        return render(request, template_name, context)

def quotation_client_email(request,acao='ERROR',send_email_sis='False'):
    if send_email_sis == True:
        template_name = "../templates/client_email.html"
        
        subject = 'MGA-Cotações - Cotação Nº: '+str(request.id)+' - '+str(request.client)[:10]+'...'
        
        emails_providers = []
        emails_providers.append(settings.EMAIL_HOST_USER)
        
        if acao == 'removida':          # E-mail enviado ao client
            message = 'Sua cotação foi '+acao+' com sucesso!.'
        elif acao == 'aprovada':        # E-mail enviado ao client    
            # Email do provider aprovado - Enviar email avisando
            provider = QuotationPrice.objects.get(quotation_number=request.id,approved=True)  

            # Emails dos providers reprovados - Enviar email avisando
            qprovider_not_approved = QuotationPrice.objects.filter(quotation_number=request.id,approved=False)
            if qprovider_not_approved:            
                emails_providers_not_approved = []
                emails_providers_not_approved.append(settings.EMAIL_HOST_USER)
                for provider_not_approved in qprovider_not_approved:
                    emails_providers_not_approved.append(provider_not_approved.quotation_provider.email)
    
            message = 'Parabéns, a '+str(provider.quotation_provider)+' foi a empresa aprovada por você! A partir de agora, este fornecedor entrará em contato, finalizando os demais detalhes e dando segmento a produção de seu planejado.'
        elif acao == 'liberada':        # E-mail enviado ao client    
            message = 'Parabéns, sua cotação foi '+acao+' com sucesso! A partir de agora é aguardar os lances de cada fornecedor e depois escolher e aprovar um deles. Em seguida da aprovação o fornecedor entrará em contato com você e juntos finalizarão o processo todo.'
           
        elif acao == 'à espera':        # E-mail enviado aos providers
            # Lista os emails dos providers para envio em lote 
            # Serão enviados somentes e-mail para os providers do mesmo estado do client e que tenha aprovaçao da plataforma para receber
            # O campo "approved=False" indica que não foi trancado o processo de orçar cotaões por parte do provider. Se for True, ele não receberá e-mail
            providers = User.objects.filter(role='provider',state=request.client.state,approved=False)
            if providers:            
                for provider in providers:
                    emails_providers.append(provider.email)
            message = 'Atenção, uma nova cotação chegou a nossa plataforma e esta '+acao+' de seu lance. '
        else:                           # E-mail enviado ao client
            message = 'Parabéns, sua cotação foi '+acao+' com sucesso! A partir de agora analisaremos e tendo alguma dúvida, entraremos em contato com você.'

        # A ação diferente de "à espera", indica analisar e preparar um link para o acesso a nível de client
        if acao != 'à espera':
            # Caminho para 0 modo de produção    
            # Link atribuido ao botão enviado no corpo do email com acesso a lista do cliente
            if settings.DEBUG == True:
                adress_link = "http://127.0.0.1:8000/client/quotation_client_list/"+str(request.client.id)
            else:
                adress_link = "http://www.mgacotacoes.com.br/client/quotation_client_list/"+str(request.client.id)

        # Sendo a ação igual "à espera", indica analisar e preparar um link para o acesso a nível de provider
        else: 
            # Caminho para 0 modo de produção    
            # Link atribuido ao botão enviado no corpo do email com acesso a cotação a ser orçada enviada a marcenaria
            if settings.DEBUG == True:
                adress_link = "http://127.0.0.1:8000/provider/quotation_provider_price/"+str(request.id)
            else:
                adress_link = "http://www.mgacotacoes.com.br/provider/quotation_provider_price/"+str(request.id)


        # Retorna o email do provider aprovado e adiciona os e-mails: da plataforma e do cliente
        emails = []
        #emails.append(settings.EMAIL_HOST_USER)     # E-mail da plataforma

        # Somente pegar o e-mail do cliente, quando o envio não for exclusivos aos providers
        if acao != 'à espera':
            emails.append(request.client.email)     # E-mail do cliente
        else:
            emails.append(settings.EMAIL_HOST_USER)     
    
        # Se for uma ação de aprovação de cotação, enviar um e-mail ao provoder
        qvalue      = 0.00        
        qprovider   = ''
        qemail      = ''
        qphone      = ''
        if acao == 'aprovada':                      # E-mail do provider
            emails.append(provider.quotation_provider.email) 
            qvalue = provider.quotation_value
            qprovider = str(provider.quotation_provider)
            qemail = provider.quotation_provider.email
            qphone = provider.quotation_provider.phone

        # E-mail de envio da plataforma
        from_email = settings.EMAIL_HOST_USER

        context = {
            "request": request,
            "message": message,
            "value_quotation": qvalue,
            "provider_quotation": qprovider,
            "email_provider": qemail,
            "phone_provider": qphone,
            "adress_link": adress_link,
            "not_approved": False
        }
        content = render_to_string(template_name, context)

        if subject and message and from_email:
            # E-mail enviados a client e providers para todos os status 
            try:
                email = EmailMessage(
                    subject,
                    content,
                    from_email, 
                    emails,
                    emails_providers
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Problema no envio do e-mail. Tente mais tarde! - Situação Geral')

            # E-mail enviado para os providers reprovados
            if acao == 'aprovada':
                message = 'Aviso!!! Esta cotação foi aprovada para outra MARCENARIA. Nós da MGA Cotações agradecemos sua participação nesta cotação e esperamos que você possa sempre contribuir dando seu orçamento a novas cotações.'

                context = {
                    "request": request,
                    "message": message,
                    "value_quotation": qvalue,
                    "provider_quotation": qprovider,
                    "email_provider": qemail,
                    "phone_provider": qphone,
                    "adress_link": adress_link,
                    "not_approved": True
                    }
                content = render_to_string(template_name, context)

                try:
                    email = EmailMessage(
                        subject,
                        content,
                        from_email, 
                        emails_providers_not_approved
                    )
                    email.content_subtype = "html"
                    email.send(fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Problema no envio do e-mail. Tente mais tarde! - Situação Específica')


            return redirect("qnow_client:quotation_client_list", request.client_id)
        else:
            return redirect("qnow_client:quotation_client_list", request.client_id)

# Lista a cotação do cliente a ser removida
@login_required
def quotation_client_delete(request, quotation_id=0, action='filter'):
    # Pesquisa as cotações do usuário logago
    if action == 'search':
        quotation = Quotation.objects.filter(id=quotation_id)
        template_name = "../templates/client_quotation_delete.html"
        message = str(request.user) + ', deseja realmente remover esta cotação?'

        context = { "active_page_client_provider": "active",
                    "message": message,
                    "acao": "Enviar", 
                    "quotation": quotation}
        return render(request, template_name, context)

    if action == 'delete':
        quotation = Quotation.objects.get(id=quotation_id)

        # Verifica se o usuário logado é o mesmo requisitado
        if quotation.client_id != request.user.id:
            response = render_to_response('404.html')
            response.status_code = 404
            return response

        quotation.removed = True
        quotation.save()                
        
        # Após excluir, enviar um email ao cliente e uma mensagem na tela
        messages.add_message(request, messages.INFO, 'Cotação Nº: '+str(quotation.id)+' removida com sucesso!')
        t2 = threading.Thread(target=quotation_client_email, args=(quotation,'removida',settings.SEND_EMAIL_SIS))
        t2.start()
        if settings.SEND_EMAIL_SIS == True:
            messages.add_message(request, messages.INFO, 'Verifique sua conta de e-mail.')
        return redirect("qnow_client:quotation_client_list", quotation.client_id)


#Envia o comentário e demais dados após o cliente receber o produto
def quotation_client_comment(request,quotation_id=0):
    template_name = "../templates/client_email_comment.html"

    if request.POST.get('comment_client_quotation'):
        # Set o texto do comentário dado na cotação do cliente já aprovada
        Quotation.objects.filter(pk=quotation_id,removed=False).update(comment=request.POST.get('comment_client_quotation'))

        subject = 'MGA-Cotações - Cotação Nº: '+str(quotation_id)+' - '+str(request.user)
        message = 'Obrigado pelo seu comentário!'

        # Get do lance aprovado para envio de email ao provider ganhador
        quotation_price = QuotationPrice.objects.get(quotation_number=quotation_id,approved=True)  

        # Dados da cotação, pois o request aqui é da tabela de orçamentos
        quotation = Quotation.objects.get(pk=quotation_id,removed=False)

        # Link atribuido ao botão enviado no corpo do email com acesso a lista do cliente
        if settings.DEBUG == True:
            adress_link = "http://127.0.0.1:8000/client/quotation_client_list/"+str(quotation.client.id)
        else:
            adress_link = "http://www.mgacotacoes.com.br/client/quotation_client_list/"+str(quotation.client.id)

        from_email = settings.EMAIL_HOST_USER
        context = {
            "request":          quotation,                                    # Quotação do cliente
            "request_provider": quotation_price,                              # Orçamento do provider
            "message":          message,                                      # Messagem de alerta
            "comment":          request.POST.get('comment_client_quotation'), # Dúvida do provider
            "adress_link":      adress_link
            }
        content = render_to_string(template_name, context)
        if subject and message and from_email and quotation:
            try:
                email = EmailMessage(
                    subject,
                    content,
                    from_email, 
                    [quotation_price.quotation_provider.email],
                    [from_email]
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
            except BadHeaderError:
                # Alerta de que ocorreu um erro no envio do e-mail
                messages.add_message(request, messages.INFO, 'Problema no envio do comentário referente a Cotação Nº: '+str(quotation.id)+'! Tente mais tarde!')
                return redirect("qnow_client:quotation_client_list", quotation.client.id)

            # Após o envio, deixar uma msg na tela 
            messages.add_message(request, messages.INFO, 'Comentário da Cotação Nº: '+str(quotation.id)+' enviado com sucesso!')
            return redirect("qnow_client:quotation_client_list", quotation.client.id)
        else:
            # Alerta de que faltou dados para o envio do comentário
            messages.add_message(request, messages.INFO, 'Falta de informações para envio do seu comentário referente a Cotação Nº: '+str(quotation.id)+'! Tente mais tarde!')
            return redirect("qnow_client:quotation_client_list", quotation.client.id)
    else:
        return redirect("qnow_client:quotation_client_list", quotation.client.id)        


