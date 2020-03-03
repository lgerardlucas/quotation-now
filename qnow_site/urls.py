from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'qnow_site'

urlpatterns = [
    path('', views.site ,name='site'),
    path('accounts/login/', views.site ,name='site'), 
    path('contact/', views.contact ,name='contact'),
    path('about/', views.about ,name='about'),
    path('blog/', views.blog ,name='blog'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

""" 
O path accounts/login foi usado, para o acesso ao site principal e não a tela de login.
Isto porque, esta plataforma acessa dois tipos de login, o client e provider, para tal,
foram criadas rotas diferentes. Mas ao recuperar a senha, o link padrão, leva para o 
escrito acima e redirecionei ele para abrir o site 
"""