# Generated by Django 4.2.1 on 2023-05-31 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0012_cartitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
    ]
