# Generated by Django 3.2 on 2023-05-24 03:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_progress', '0042_projectprogress_due_date_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(default='', max_length=80)),
                ('completed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('interval_between_team_task', models.DurationField(blank=True, null=True)),
                ('interval_between_my_task', models.DurationField(blank=True, null=True)),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
