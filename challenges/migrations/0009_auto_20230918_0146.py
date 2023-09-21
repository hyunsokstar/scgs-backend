# Generated by Django 3.2 on 2023-09-17 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0008_auto_20230918_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationresult',
            name='challenger',
        ),
        migrations.AddField(
            model_name='evaluationresult',
            name='evaluate_criteria_description',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.RemoveField(
            model_name='evaluationresult',
            name='challenge',
        ),
        migrations.AddField(
            model_name='evaluationresult',
            name='challenge',
            field=models.ManyToManyField(related_name='challengers', to='challenges.Challenge'),
        ),
        migrations.AlterField(
            model_name='evaluationresult',
            name='result',
            field=models.CharField(choices=[('pass', 'Pass'), ('fail', 'Fail'), ('undecided', 'Undecided')], default='Pass', max_length=20),
        ),
        migrations.AlterField(
            model_name='evaluationresult',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Challenger',
        ),
    ]