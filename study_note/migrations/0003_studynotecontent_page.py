# Generated by Django 3.2 on 2023-04-24 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0002_studynotecontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='studynotecontent',
            name='page',
            field=models.IntegerField(default=1),
        ),
    ]
