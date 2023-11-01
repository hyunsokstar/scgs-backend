# Generated by Django 3.2 on 2023-11-01 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0031_auto_20231101_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentforerrorreport',
            name='error_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='study_note.errorreportforstudynote'),
        ),
        migrations.AlterField(
            model_name='errorreportforstudynote',
            name='study_note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='error_report_list', to='study_note.studynote'),
        ),
    ]
