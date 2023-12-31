# Generated by Django 4.2.5 on 2023-12-19 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notification', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_notification', to='product.product'),
        ),
    ]
