# Generated by Django 4.0.5 on 2022-06-17 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acount', '0002_user_confirm_password_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirm_password',
        ),
    ]
