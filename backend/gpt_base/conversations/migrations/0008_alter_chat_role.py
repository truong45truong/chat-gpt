# Generated by Django 4.2 on 2023-04-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0007_alter_chat_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='role',
            field=models.CharField(default='user', max_length=100),
        ),
    ]
