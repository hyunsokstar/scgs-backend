# Generated by Django 3.2 on 2023-12-08 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0039_auto_20231208_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studynote',
            name='first_category',
            field=models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('full-stack', 'FullStack')], default='frontend', max_length=20),
        ),
    ]