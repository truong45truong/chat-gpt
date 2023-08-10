# Generated by Django 4.2 on 2023-06-07 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_initial'),
        ('documents', '0003_templates_question_asked'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents_members', to='members.members'),
        ),
        migrations.AddField(
            model_name='documents',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]