# Generated by Django 3.2 on 2023-11-15 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0034_bookmarkforstudynote_likeforstudynote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmarkforstudynote',
            old_name='liked_at',
            new_name='bookmarked_at',
        ),
    ]
