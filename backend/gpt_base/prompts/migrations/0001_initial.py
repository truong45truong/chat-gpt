# Generated by Django 4.2 on 2023-05-10 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members_prompts', to='members.members')),
            ],
            options={
                'verbose_name_plural': 'prompts',
                'db_table': 'prompts',
            },
        ),
    ]
