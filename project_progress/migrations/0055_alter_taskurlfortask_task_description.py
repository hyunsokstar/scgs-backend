# Generated by Django 3.2 on 2023-05-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0054_taskurlfortask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskurlfortask',
            name='task_description',
            field=models.CharField(default='', max_length=30),
        ),
    ]
