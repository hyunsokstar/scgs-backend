# Generated by Django 3.2 on 2023-03-31 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech_note', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechNoteContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.CharField(blank=True, max_length=50, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
