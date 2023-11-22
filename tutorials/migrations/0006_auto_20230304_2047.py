# Generated by Django 3.2 on 2023-03-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0005_tutorial_tutorial_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorial',
            name='open_chat_url',
        ),
        migrations.RemoveField(
            model_name='tutorial',
            name='teacher',
        ),
        migrations.AddField(
            model_name='tutorial',
            name='frontend_framework_option',
            field=models.CharField(blank=True, choices=[('django_drf', 'django_drf'), ('fast_api', 'fast_api'), ('sptring_boot', 'spring_boot'), ('express', 'express'), ('nest_js', 'nest_js')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='price',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
