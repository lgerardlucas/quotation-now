# Generated by Django 2.2.2 on 2019-08-15 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0008_auto_20190815_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='stage',
            field=models.ForeignKey(on_delete=True, related_name='QuotationStage', to='qnow_client.QuotationStage'),
        ),
    ]
