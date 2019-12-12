# Generated by Django 2.2.2 on 2019-10-29 02:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qnow_client', '0036_delete_quotationprice'),
        ('qnow_provider', '0002_delete_quotationprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotationPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateField(default=datetime.date.today)),
                ('date_validate', models.DateField(blank=True, null=True)),
                ('quotation_value', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('delivery_time', models.CharField(default='', max_length=30)),
                ('form_payment', models.CharField(default='', max_length=50)),
                ('comments', models.TextField(blank=True)),
                ('quotation_number', models.ForeignKey(on_delete=True, related_name='quotation_price', to='qnow_client.Quotation')),
                ('quotation_provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation_provider', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Preço',
                'verbose_name_plural': 'Preços',
                'ordering': ['date_create'],
            },
        ),
    ]