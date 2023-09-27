# Generated by Django 3.2 on 2023-09-26 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0028_alter_evaluationcriteria_challenge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengerref',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenger_refs', to='challenges.challenge'),
        ),
    ]
