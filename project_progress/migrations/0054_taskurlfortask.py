# Generated by Django 3.2 on 2023-05-30 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0053_auto_20230530_0525'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskUrlForTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_url', models.URLField(blank=True, null=True)),
                ('task_description', models.TextField(default='', max_length=300)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_urls', to='project_progress.projectprogress')),
            ],
        ),
    ]
