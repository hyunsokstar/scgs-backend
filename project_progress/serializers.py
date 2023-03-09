from .models import ProjectProgress
from rest_framework import serializers
from requests import Response

# task
# writer 
# importance
# task_status
# password

class ProjectProgressListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "writer",
            "importance",
            "task_status",
        )

