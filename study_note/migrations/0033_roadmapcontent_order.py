# Generated by Django 3.2 on 2023-11-05 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0032_auto_20231101_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadmapcontent',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
