# Generated by Django 3.2 on 2023-04-21 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0031_projectprogress_is_success_for_cash_prize'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='is_task_for_cash_prize',
            field=models.BooleanField(default=False),
        ),
    ]
