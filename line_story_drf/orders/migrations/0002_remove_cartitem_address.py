# Generated by Django 4.1 on 2022-08-29 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='address',
        ),
    ]
