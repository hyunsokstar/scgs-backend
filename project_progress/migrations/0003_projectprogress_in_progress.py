# Generated by Django 3.2 on 2023-03-23 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0002_auto_20230320_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
