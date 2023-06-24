# Generated by Django 3.2 on 2023-06-21 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_note', '0012_alter_studynote_first_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoomForStudyNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_page', models.PositiveIntegerField()),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_list', to='study_note.studynote')),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]