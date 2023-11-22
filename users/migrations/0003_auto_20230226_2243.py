# Generated by Django 3.2 on 2023-02-26 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avatar',
            new_name='profile_image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_host',
        ),
        migrations.RemoveField(
            model_name='user',
            name='language',
        ),
    ]
