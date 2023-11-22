# Generated by Django 3.2 on 2023-03-31 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tech_note', '0002_technotecontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='technotecontent',
            name='tech_note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tech_note_contents', to='tech_note.technote'),
        ),
    ]
