# Generated by Django 4.2.1 on 2023-06-01 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0022_rename_cartitem_checkout_cart_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='cart_item',
        ),
    ]