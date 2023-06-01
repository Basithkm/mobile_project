# Generated by Django 4.2.1 on 2023-06-01 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0027_orderitem_delivary_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='orderitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='store_app.orderitem'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='delivary_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store_app.address'),
        ),
    ]