# Generated by Django 4.1.7 on 2023-06-06 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0016_story_sub_category_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_status',
            field=models.IntegerField(blank=True, help_text='1. approved, 2. Pending, 3. Unapproved', null=True),
        ),
    ]