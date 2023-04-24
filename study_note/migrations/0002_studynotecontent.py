# Generated by Django 3.2 on 2023-04-24 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_note', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyNoteContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='black', max_length=30)),
                ('file_name', models.CharField(blank=True, max_length=50, null=True)),
                ('content', models.TextField(default='black')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('study_note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_contents', to='study_note.studynote')),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
