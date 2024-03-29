# Generated by Django 3.2 on 2023-07-03 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0064_projectprogress_due_date_option_for_today'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectprogress',
            name='due_date_option_for_today',
            field=models.CharField(choices=[('until-noon', '오전까지'), ('until-evening', '오후까지'), ('until-night', '밤 늦게 까지')], default='until-noon', max_length=20),
        ),
    ]
