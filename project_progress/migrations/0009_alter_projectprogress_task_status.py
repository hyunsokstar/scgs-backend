# Generated by Django 3.2 on 2023-03-10 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0008_auto_20230310_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectprogress',
            name='task_status',
            field=models.BooleanField(default=False),
        ),
    ]
