# Generated by Django 3.2 on 2023-03-03 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0003_auto_20230303_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
