# Generated by Django 3.2 on 2023-04-10 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortCut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortcut', models.TextField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('classification', models.CharField(choices=[('front', 'Frontend'), ('back', 'Backend')], max_length=10)),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shortcuts2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
