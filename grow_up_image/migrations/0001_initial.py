# Generated by Django 4.2.5 on 2023-12-19 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrowupImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=255, upload_to='traceability/')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
