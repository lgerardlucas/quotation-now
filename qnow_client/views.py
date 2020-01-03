from django.shortcuts import render, redirect, Http404, render_to_response, get_list_or_404, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.utils.safestring import mark_safe
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError, EmailMultiAlternatives
from django.conf import settings
import uuid
import threading
from .models import Quotation, QuotationStage
from qnow_provider.models import QuotationPrice
from .forms import QuotationForm

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
@login_required
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
        quotationprice_update_row = QuotationPrice.objects.filter(pk=request.POST.get('price_id')).update(approved=True)  
resolver o envio de email para o provider ao aprovar pelo cliente uma cotação        
        # Retorna id para o stage = 4 aprovado
        quotationstage = QuotationStage.objects.get(status=4)

        # Alterando o stage da cotação para 4 = aprovado 
        Quotation.objects.filter(pk=quotationprice_id).update(stage_id=quotationstage.id)

        # Após aprovar, enviar um email ao cliente e a marcenaria e uma mensagem na tela
        messages.add_message(request, messages.INFO, 'Cotação Nº: '+str(quotationprice_id)+' aprovada com sucesso!')

        t2 = threading.Thread(target=quotation_client_email, args=(Quotation,'aprovada',settings.SEND_EMAIL_SIS))
        t2.start()

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
        
        subject = 'Quotation-NOW - Cotação Nº: '+str(request.id)+' - '+str(request.client)
        if acao == 'removida':
            message = 'Sua cotação foi '+acao+' com sucesso!.'
        elif acao == 'aprovada':            
            message = 'Parabéns, sua cotação foi '+acao+' com sucesso!\nAguarde o contato do fornecedor escolhido.'
        else:
            message = 'Parabéns, sua cotação foi '+acao+' com sucesso!\nA partir de agora analisaremos e tendo alguma dúvida, entraremos em contato com você.'
            
        from_email = settings.EMAIL_HOST_USER

        context = {
            "request": request,
            "message":message,
            }
        content = render_to_string(template_name, context)


        if subject and message and from_email:
            try:
                email = EmailMessage(
                    subject,
                    content,
                    from_email, 
                    [request.client.email],
                    ['lgerardlucas@gmail.com']
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Problema no envio do e-mail. Tente mais tarde!')
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

