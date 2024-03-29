# Generated by Django 3.2 on 2023-03-30 01:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TechNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(blank=True, choices=[('create', 'Create'), ('read', 'Read'), ('update', 'Update'), ('delete', 'Delete'), ('boiler_plate', 'BoilerPlate'), ('libray_example', 'LibraryExample')], max_length=15, null=True)),
                ('like_count', models.IntegerField(default=0)),
                ('view_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tech_notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
