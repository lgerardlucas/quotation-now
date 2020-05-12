from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, BadHeaderError, EmailMultiAlternatives
from .models import Contact
from django.template import Context, RequestContext
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings
from qnow_user.models import User
from qnow_client.models import Quotation
from django.db.models import Q
import datetime

# Transforma a letra de cada palavra em maiusculo
def capitalize_text(name):
    p = ['da', 'de', 'di', 'do', 'du', 'para']
    name = name.lower()
    items = []
    for item in name.split():
        if not item in p:
            item = item.capitalize()
        items.append(item)
    return ' '.join(items)


# Acessa a tela principal do site
def site(request):
    # Executa logout quanto fora da área de cotação
    logout(request)

    # Pesquisa as cotações com status = 2 a 6 
    quotations = Quotation.objects.filter(stage_id__status__range=[2, 6], removed=False).filter((Q(view_environment_quotation_home=True, image_environment__isnull=False) | Q(view_project_quotation_home=True, image_project__isnull=False))).order_by('-date_create', '-id')[:20]

    context = {'active_page_site': 'active',
                'quotation_list': quotations
        }
    return render(request, '../templates/index.html',context)

# Acesso a tela de sobre do site  
def about(request):
    # Executa logout quanto fora da área de cotação
    logout(request)

    context = {'active_page_about' : 'active'}
    return render(request, '../templates/about.html',context)

# Acesso a tela de blog
def blog(request):
    # Executa logout quanto fora da área de cotação
    logout(request)

    context = {'active_page_blog' : 'active'}
    return render(request, '../templates/blog.html',context)

# Gravar o e-mail enviado pela tela de contato
def contact(request):
    template_name = '../templates/contact.html'
    form =  ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            Contact = form.save(commit=False)
            Contact.name = capitalize_text(Contact.name)
            Contact.email_send = Contact.email_send.lower()
            form.save()

            # Após salvar, enviar um email ao cliente e uma mensagem na tela
            message_bory = 'E-mail enviado com sucesso!'
            contact_email(Contact)
            messages.add_message(request, messages.SUCCESS, message_bory)

            form = ContactForm()
        else:
            form = ContactForm(request.POST)
    else:
        form = ContactForm()
    context = {
        'active_page_contact' : 'active',
        'form': form
    }
    # Executa logout quanto fora da área de cotação
    logout(request)
    
    return render(request, template_name,context)

# Envia um email referente ao contato do site
def contact_email(request):
    template_name = "../templates/contact_email.html"
    subject = 'MGA-Cotações'
            
    from_email = settings.EMAIL_HOST_USER
    context = {
        "name_send": request.name,
        "assunto_send": request.subject_send,
        "message_send": request.message_send,
        }

    content = render_to_string(template_name, context)

    if subject and from_email:
        try:
            if request.copy_send:
                email_copy = request.email_send
            email = EmailMessage(
                subject,
                content,
                from_email, 
                [email_copy,'lgerardlucas@gmail.com'],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Problema no envio do e-mail. Tente mais tarde!')
