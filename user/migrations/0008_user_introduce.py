# Generated by Django 4.2.5 on 2023-11-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='introduce',
            field=models.TextField(default=None, null=True),
        ),
    ]
