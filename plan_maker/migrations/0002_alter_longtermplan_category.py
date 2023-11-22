# Generated by Django 3.2 on 2023-05-07 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_maker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='longtermplan',
            name='category',
            field=models.CharField(choices=[('month', '한 달'), ('week', '일주일'), ('day', '하루')], default='month', max_length=10),
        ),
    ]
