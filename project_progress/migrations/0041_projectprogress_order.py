# Generated by Django 3.2 on 2023-05-21 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0040_remove_projectprogress_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='order',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
