# Generated by Django 3.2 on 2023-06-02 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_progress', '0061_delete_testersfortestforextratask'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestersForTestForExtraTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testers_for_test_for_extra_task', to='project_progress.testforextratask')),
                ('tester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
