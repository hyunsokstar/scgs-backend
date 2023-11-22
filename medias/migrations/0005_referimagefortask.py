# Generated by Django 3.2 on 2023-03-20 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0002_auto_20230320_2019'),
        ('medias', '0004_photoforprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferImageForTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField()),
                ('task', models.ForeignKey(blank=True, max_length=200, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_images', to='project_progress.projectprogress')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
