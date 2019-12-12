# Generated by Django 2.2.2 on 2019-08-20 14:57

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0014_auto_20190820_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='image_environment',
            field=cloudinary.models.CloudinaryField(blank=True, default='', max_length=255, null=True, verbose_name='image_environment'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='image_project',
            field=cloudinary.models.CloudinaryField(blank=True, default='', max_length=255, null=True, verbose_name='image_project'),
        ),
    ]