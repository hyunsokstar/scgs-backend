# Generated by Django 3.2 on 2023-03-26 15:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_progress', '0010_supplementarytask_orginal_task'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SupplementaryTask',
            new_name='ExtraTask',
        ),
    ]
