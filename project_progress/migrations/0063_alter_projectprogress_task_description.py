# Generated by Django 3.2 on 2023-06-29 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0062_testersfortestforextratask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectprogress',
            name='task_description',
            field=models.TextField(blank=True, default='', max_length=300, null=True),
        ),
    ]
