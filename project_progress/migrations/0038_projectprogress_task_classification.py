# Generated by Django 3.2 on 2023-05-06 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_progress', '0037_rename_is_for_urgent_projectprogress_is_task_for_urgent'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprogress',
            name='task_classification',
            field=models.CharField(choices=[('crud', 'CRUD 작업'), ('new-future', '새로운 기능 개발'), ('trouble-shooting', '문제 해결 작업'), ('ui-task', 'UI 작업'), ('refactoring', '리팩토링 작업'), ('optimization', '최적화 작업'), ('boiler-plate', '보일러 플레이트 만들기'), ('test-code', '테스트 코드 작성')], default='crud', max_length=20),
        ),
    ]
