# Generated by Django 4.2 on 2023-04-20 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TranslateTypesMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('delete_flag', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'm_translate_types',
            },
        ),
    ]
