# Generated by Django 3.2 on 2023-09-19 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_alter_surveyoption_survey'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyanswer',
            old_name='writer',
            new_name='participant',
        ),
    ]
