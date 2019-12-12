from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'qnow_site'

urlpatterns = [
    path('', views.site ,name='site'),
    path('contact/', views.contact ,name='contact'),
    path('about/', views.about ,name='about'),
    path('blog/', views.blog ,name='blog'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

