# Generated by Django 3.2 on 2023-10-30 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tech_note', '0008_technote_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('sub_title', models.CharField(max_length=50)),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loadmaps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
