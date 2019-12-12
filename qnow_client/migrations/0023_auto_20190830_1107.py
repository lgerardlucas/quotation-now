# Generated by Django 2.2.2 on 2019-08-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0022_auto_20190830_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='house_type',
            field=models.CharField(choices=[('Apartamento', 'Apartamento'), ('Casa', 'Casa'), ('Comercial', 'Comercial'), ('Escritório', 'Escritório'), ('Outro', 'Outro')], default='Casa', help_text='Nos informe o tipo do seu imóvel(Apartamento, casa...)', max_length=20),
        ),
    ]
