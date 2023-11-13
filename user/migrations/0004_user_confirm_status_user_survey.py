# Generated by Django 4.2.5 on 2023-11-13 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirm_status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('PENDING', 'PENDING'), ('DONE', 'DONE')], default='NONE'),
        ),
        migrations.AddField(
            model_name='user',
            name='survey',
            field=models.JSONField(default=dict),
        ),
    ]
