# Generated by Django 3.2 on 2023-04-04 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_progress', '0020_rename_task_testersfortest_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testersfortest',
            name='tester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
