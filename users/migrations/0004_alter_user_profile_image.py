# Generated by Django 3.2 on 2023-02-26 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230226_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
