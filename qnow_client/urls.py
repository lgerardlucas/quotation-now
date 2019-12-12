from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.conf.urls import handler404,  handler500


app_name = 'qnow_client'

urlpatterns = [
  path('quotation_client/', views.quotation_client ,name='quotation_client'),
  path('quotation_client_list/<int:client_id>', views.quotation_client_list ,name='quotation_client_list'),
  path('quotation_client_edit/<int:quotation_id>', views.quotation_client_edit ,name='quotation_client_edit'),
  path('quotation_client_delete/<int:quotation_id>/<str:action>', views.quotation_client_delete ,name='quotation_client_delete'),
  path('quotation_client_email/', views.quotation_client_email ,name='quotation_client_email'),
  path('quotation_client_approved/<int:quotationprice_id>', views.quotation_client_approved ,name='quotation_client_approved'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'qnow_client.views.error_404_view'
handler500 = 'qnow_client.views.error_500_view'