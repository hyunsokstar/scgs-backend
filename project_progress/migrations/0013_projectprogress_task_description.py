# Generated by Django 3.2 on 2023-03-28 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0012_rename_orginal_task_extratask_original_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='task_description',
            field=models.TextField(default='', max_length=300),
        ),
    ]
