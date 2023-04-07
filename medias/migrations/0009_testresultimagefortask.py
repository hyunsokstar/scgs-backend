# Generated by Django 3.2 on 2023-04-07 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0023_taskcomment_is_edit_mode'),
        ('medias', '0008_rename_image_file_referimagefortask_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResultImageForTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.URLField()),
                ('task', models.ForeignKey(blank=True, max_length=200, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_result_images', to='project_progress.testfortask')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
