# Generated by Django 2.2.2 on 2020-01-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_user', '0012_user_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='approved',
            field=models.BooleanField(blank=True, default=True, verbose_name='Mov/Autorizada'),
        ),
    ]
