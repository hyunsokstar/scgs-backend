# Generated by Django 3.2 on 2023-05-05 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0035_projectprogress_check_for_cash_prize'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='is_for_urgent',
            field=models.BooleanField(default=False),
        ),
    ]
