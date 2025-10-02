from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['owner', 'name', 'description', 'category', 'init_hour', 'end_hour', 'status']