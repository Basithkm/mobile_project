# Generated by Django 4.2.1 on 2023-06-01 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0021_alter_checkout_cartitem_alter_checkout_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='cartitem',
            new_name='cart_item',
        ),
    ]