# Generated by Django 3.2 on 2023-05-08 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan_maker', '0006_alter_longtermplancontents_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='longtermplancontents',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan_contents', to='plan_maker.longtermplan'),
        ),
    ]