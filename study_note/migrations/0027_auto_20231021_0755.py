# Generated by Django 3.2 on 2023-10-20 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0026_auto_20231021_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='cowriterforstudynote',
            name='current_page',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cowriterforstudynote',
            name='task_description',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]
