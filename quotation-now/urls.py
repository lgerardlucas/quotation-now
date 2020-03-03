from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import re
from django.contrib.auth import urls,views


urlpatterns = [
    path('', include('qnow_site.urls',namespace='site')),
    path('admin/', admin.site.urls),
    path('accounts/', include('qnow_user.urls',namespace='accounts')),
    path('client/', include('qnow_client.urls',namespace='client')),
    path('provider/', include('qnow_provider.urls',namespace='provider')),
    path('', include('django.contrib.auth.urls')),
    ]

if settings.DEBUG:
    import debug_toolbar
    from django.urls import include
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls,namespace='debug')),
    ] + urlpatterns


#admin.site.site_header = 'Quotation-NOW'    
#admin.site.index_title = 'Q-NOW(Administrador)'    
#admin.site.site_title = 'Q-NOW'    

admin.site.site_header = 'MGA-Cotações'    
admin.site.index_title = 'MGA(Administrador)'    
admin.site.site_title = 'MGA'    
