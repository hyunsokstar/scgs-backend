# Generated by Django 3.2 on 2023-02-28 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_skill_for_framework'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skillforframework',
            old_name='skil_name',
            new_name='frame_work_name',
        ),
    ]
