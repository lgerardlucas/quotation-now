# Generated by Django 2.2.2 on 2019-08-30 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_user', '0006_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, verbose_name='Usuário'),
        ),
    ]
