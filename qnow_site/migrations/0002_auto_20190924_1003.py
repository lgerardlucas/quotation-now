# Generated by Django 2.2.2 on 2019-09-24 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='copy_send',
            field=models.BooleanField(default=True, verbose_name='Enviar cópia'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email_send',
            field=models.EmailField(max_length=100, verbose_name='E-mail*'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message_send',
            field=models.TextField(verbose_name='Mensagem*'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nome*'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject_send',
            field=models.CharField(max_length=100, verbose_name='Assunto*'),
        ),
    ]