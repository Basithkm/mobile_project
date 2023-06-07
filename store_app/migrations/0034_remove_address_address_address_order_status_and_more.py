# Generated by Django 4.2.1 on 2023-06-06 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0033_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('PACKED', 'Packed'), ('DELIVERED', 'Delivered')], default='ACCEPTED', max_length=20),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]