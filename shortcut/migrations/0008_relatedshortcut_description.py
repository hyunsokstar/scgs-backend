# Generated by Django 3.2 on 2023-05-13 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcut', '0007_auto_20230513_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatedshortcut',
            name='description',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
