# Generated by Django 3.2 on 2023-02-28 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_skil_name_skillforframework_frame_work_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
    ]
