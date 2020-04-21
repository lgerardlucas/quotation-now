from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string, get_template
from django.utils.safestring import mark_safe
from django.template import Context, RequestContext
from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import User
import threading
from qnow_client.models import Quotation
from .forms import RegisterForm, EditAccountForm

# Redirect usado pelo template quando client para o correto redirect
def login_client_start(request, *args, **kwargs):
    settings.LOGIN_REDIRECT_URL = 'qnow_client:quotation_client'
    return redirect('qnow_user:login_client')

# Redirect usado pelo template quando provider para o correto redirect
def login_provider_start(request, *args, **kwargs):
    settings.LOGIN_REDIRECT_URL = 'qnow_provider:quotation_provider'
    return redirect('qnow_user:login_provider')

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

# def usada somente para registrar o usuários 
def register(request, origin, *args, **kwargs):
    template_name = '../templates/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = origin
            user.email = user.email.lower()
            user.username = capitalize_text(user.username)
            '''
            # Por padrão, o provider estará inativo quando no primeiro cadastro
            if origin != 'client':
               user.approved = False
            else:
               user.approved = True
            '''
            user.save()
            user = authenticate(
                email=user.email, password=form.cleaned_data['password1'],backend='django.contrib.auth.backends.ModelBackend'
            )
            login(request, user)

            # Envia um e-mail ao cliente após o cadastro
            t1 = threading.Thread(target=user_email, args=(user,'cadastrado',settings.SEND_EMAIL_SIS))
            t1.start()
            #user_email(user,'cadastrado',settings.SEND_EMAIL_SIS)
            
            if origin == 'client':
                return redirect('qnow_client:quotation_client')
            else:
                return redirect('qnow_provider:quotation_provider')

    else:
        form = RegisterForm()

    context = {
        'active_page_client_provider':'active',
        'origin': origin,
        'form': form
    }
    return render(request, template_name, context)


def user_email(request,acao='ERROR',send_email_sis='False'):
    if send_email_sis == True:
        template_name = "../templates/user_email.html"
        subject = 'MGA-Cotações: '+str(request.username)+' '+acao+' com sucesso!'
        message = 'Parabéns, seu cadastro foi registrado com sucesso!'
        from_email = settings.EMAIL_HOST_USER

        context = {
            "request": request,
            "message":message
            }
        content = render_to_string(template_name, context)

        if subject and message and from_email:
            try:
                email = EmailMessage(
                    subject,
                    content,
                    from_email, 
                    [request.email],
                    ['lgerardlucas@gmail.com']
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Problema no envio do e-mail. Tente mais tarde!')
  