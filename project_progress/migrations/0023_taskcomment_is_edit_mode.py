# Generated by Django 3.2 on 2023-04-06 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0022_taskcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcomment',
            name='is_edit_mode',
            field=models.BooleanField(default=False),
        ),
    ]
