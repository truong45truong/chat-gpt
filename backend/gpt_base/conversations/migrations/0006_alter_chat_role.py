# Generated by Django 4.2 on 2023-04-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0005_remove_chat_is_inverse_chat_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='role',
            field=models.IntegerField(default='user'),
        ),
    ]