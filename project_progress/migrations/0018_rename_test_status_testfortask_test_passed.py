# Generated by Django 3.2 on 2023-03-29 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0017_rename_task_method_testfortask_test_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testfortask',
            old_name='test_status',
            new_name='test_passed',
        ),
    ]
