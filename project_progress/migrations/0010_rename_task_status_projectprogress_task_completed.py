# Generated by Django 3.2 on 2023-03-10 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0009_alter_projectprogress_task_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectprogress',
            old_name='task_status',
            new_name='task_completed',
        ),
    ]
