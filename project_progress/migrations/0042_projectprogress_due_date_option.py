# Generated by Django 3.2 on 2023-05-21 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0041_projectprogress_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='due_date_option',
            field=models.CharField(choices=[('morning_tasks', '아침 작업'), ('afternoon_tasks', '오후 작업'), ('night_tasks', '밤 작업')], default='morning_tasks', max_length=20),
        ),
    ]
