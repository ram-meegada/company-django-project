# Generated by Django 4.1.7 on 2023-05-16 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0007_book_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_availability_duration',
        ),
    ]
