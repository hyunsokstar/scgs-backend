# Generated by Django 3.2 on 2023-03-10 08:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0006_alter_projectprogress_started_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectprogress',
            name='started_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
