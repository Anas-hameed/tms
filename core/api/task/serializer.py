"""Serializer class to convert json data for task"""

from rest_framework import serializers

from core.models import Task, TaskCompletion
from core.api.feedback.serializer import FeedbackUserSerializer


class TaskCompletionSerializer(serializers.ModelSerializer):
    """task completion serializer to serialize model fields"""

    class Meta:
        """meta attribute specified for the serializer"""

        model = TaskCompletion
        fields = '__all__'
        read_only_fields = ['user', 'task']


class TaskRelationSerializer(serializers.ModelSerializer):
    """serializer class for the task"""

    class Meta:
        """a class to specify the meta attribute"""

        model = Task
        fields = [
            'id',
            'name',
            'description',
            'attactment_link',
            'module',
            'file',
        ]
        read_only_fields = ['module']


class TaskSerializer(serializers.ModelSerializer):
    """serializer class for the task"""

    class Meta:
        """a class to specify the meta attribute"""

        model = Task
        fields = [
            'id',
            'name',
            'description',
            'attactment_link',
            'file',
            'module',
        ]
        read_only_fields = ['module']


class TaskFeedbackSerializer(serializers.ModelSerializer):
    """serializer class for the task"""

    feedback = FeedbackUserSerializer(many=True, read_only=True)
    task_complete = TaskCompletionSerializer(read_only=True)

    class Meta:
        """a class to specify the meta attribute"""

        model = Task
        fields = [
            'id',
            'name',
            'description',
            'attactment_link',
            'module',
            'file',
            'feedback',
            'task_complete',
        ]
        read_only_fields = [
            'module',
            'feedback',
            'task_complete',
        ]
