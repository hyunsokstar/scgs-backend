# Generated by Django 3.2 on 2023-04-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0028_auto_20230420_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectprogress',
            name='cash_prize',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='projectprogress',
            name='is_urgent_request',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]