# Generated by Django 3.2 on 2023-09-24 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0018_challengeresult_challenger'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengeresult',
            name='github_url1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='challengeresult',
            name='github_url2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='challengeresult',
            name='note_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]