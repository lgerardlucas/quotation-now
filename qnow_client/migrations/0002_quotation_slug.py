# Generated by Django 2.2.2 on 2019-08-08 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='slug',
            field=models.SlugField(default='page-slug', max_length=150, unique=True),
        ),
    ]
