# Generated by Django 3.2 on 2023-03-20 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0005_referimagefortask'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referimagefortask',
            old_name='image',
            new_name='image_url',
        ),
    ]
