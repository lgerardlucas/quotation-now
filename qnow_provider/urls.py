from django.urls import path, include
from . import views

app_name = 'qnow_provider'

urlpatterns = [
  path('quotation_provider/', views.quotation_provider ,name='quotation_provider'),
  path('quotation_provider_detail/<int:quotation_id>', views.quotation_provider_detail ,name='quotation_provider_detail'),
  path('quotation_provider_price/<int:quotation_id>', views.quotation_provider_price ,name='quotation_provider_price'),
  path('quotation_provider_price_post/<int:quotation_id>', views.quotation_provider_price_post ,name='quotation_provider_price_post'),
  path('quotation_provider_email_inquire/<int:quotation_id>', views.quotation_provider_email_inquire ,name='quotation_provider_email_inquire'),
]
