# Generated by Django 3.2 on 2023-04-12 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcut', '0005_alter_shortcut_shortcut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortcut',
            name='shortcut',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]