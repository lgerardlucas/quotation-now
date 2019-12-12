from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView,LogoutView
from . import views


app_name = 'qnow_user'

urlpatterns = [
    path('login_client_start/', views.login_client_start, kwargs={'origin': 'client' }, name='login_client_start'),
    path('login_provider_start/', views.login_provider_start, kwargs={'origin': 'provider' }, name='login_provider_start'),
    
    path('login_client/',   LoginView.as_view(template_name='../templates/login.html',
                                     extra_context={'next':'qnow_client:quotation_client',
                                                    'origin':'client',
                                                    'active_page_client_provider':'active'
                                                    }
                                    ), name="login_client"),
    path('login_provider/', LoginView.as_view(template_name='../templates/login.html',
                                     extra_context={'next':'qnow_provider:quotation_provider',
                                                    'origin':'provider',
                                                    'active_page_client_provider':'active'
                                                    }
                                    ), name="login_provider"),

    path('logout/', LogoutView.as_view(template_name='../templates/index.html',
                                    extra_context={'next_page':'qnow_site:site',
                                                   'active_page_site': 'active',
                                    }),name='logout'),

    path('register_client/', views.register, kwargs={'origin': 'client' }, name='register_client'),
    path('register_provider/', views.register, kwargs={'origin': 'provider' }, name='register_provider'),
]
