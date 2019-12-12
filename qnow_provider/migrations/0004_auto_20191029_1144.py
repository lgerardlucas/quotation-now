# Generated by Django 2.2.2 on 2019-10-29 14:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0003_quotationprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Comentário da Marcenaria'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='date_create',
            field=models.DateField(default=datetime.date.today, verbose_name='Data da Cotação'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(blank=True, null=True, verbose_name='Validade da Cotação'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='delivery_time',
            field=models.CharField(default='', max_length=30, verbose_name='Prazo de Entrega'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='form_payment',
            field=models.CharField(default='', max_length=50, verbose_name='Forma de Pagamento'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='quotation_number',
            field=models.ForeignKey(on_delete=True, related_name='quotation_price', to='qnow_client.Quotation', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='quotation_provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation_provider', to=settings.AUTH_USER_MODEL, verbose_name='Marcenaria'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='quotation_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor da Cotação'),
        ),
    ]