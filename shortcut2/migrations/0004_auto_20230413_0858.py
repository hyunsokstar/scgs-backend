# Generated by Django 3.2 on 2023-04-12 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcut2', '0003_alter_shortcut_shortcut'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='shortcut',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='shortcuts', to='shortcut2.Tags'),
        ),
    ]
