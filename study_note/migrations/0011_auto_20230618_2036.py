# Generated by Django 3.2 on 2023-06-18 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_note', '0010_studynotebriefingboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='studynote',
            name='first_category',
            field=models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('challenge', 'Challenge'), ('boiler-plate', 'Boiler Plate')], default='frontend', max_length=20),
        ),
        migrations.AddField(
            model_name='studynote',
            name='second_category',
            field=models.CharField(choices=[('tutorial', 'Tutorial'), ('framework', 'Framework'), ('library', 'Library'), ('boiler-plate', 'Boiler Plate'), ('sample-code', 'Sample Code'), ('code-review', 'Code Review'), ('programming-language', 'Programming Language'), ('challenge', 'Challenge')], default='tutorial', max_length=20),
        ),
    ]
