# Generated by Django 4.1.7 on 2023-05-18 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0015_alter_story_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='sub_category_status',
            field=models.IntegerField(blank=True, help_text='1. approved, 2. Pending, 3. Unapproved', null=True),
        ),
    ]
