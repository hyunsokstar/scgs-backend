# Generated by Django 3.2 on 2023-05-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_maker', '0004_longtermplancontents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='longtermplancontents',
            name='type',
            field=models.CharField(choices=[('project', 'Project'), ('task', 'Task')], default='task', max_length=20),
        ),
    ]