# Generated by Django 3.2 on 2023-03-20 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0006_rename_image_referimagefortask_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referimagefortask',
            old_name='image_url',
            new_name='image_file',
        ),
    ]
