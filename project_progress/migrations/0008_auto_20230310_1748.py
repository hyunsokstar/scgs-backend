# Generated by Django 3.2 on 2023-03-10 08:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0007_alter_projectprogress_started_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectprogress',
            name='started_at',
        ),
        migrations.AddField(
            model_name='projectprogress',
            name='started_at_utc',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]