# Generated by Django 4.2.5 on 2023-11-13 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to=settings.AUTH_USER_MODEL),
        ),
    ]
