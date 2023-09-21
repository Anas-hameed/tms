"""Serializer class to convert json data for module"""

from rest_framework import serializers

from core.models import Module, ModuleCompletion
from core.api.task.serializer import TaskRelationSerializer


class ModuleCompletionSerializer(serializers.ModelSerializer):
    """module completion serializer to serialize model fields"""

    class Meta:
        """meta attribute specified for the serializer"""

        model = ModuleCompletion
        fields = '__all__'
        read_only_fields = ['user', 'module']


class ModuleTaskSerializer(serializers.ModelSerializer):
    """serializer for the training plan module"""

    task = TaskRelationSerializer(many=True, read_only=True)
    module_complete = ModuleCompletionSerializer(read_only=True)

    class Meta:
        """a class to specify the meta attribute"""

        model = Module
        fields = [
            'id',
            'name',
            'descrption',
            'attactment_link',
            'create_date',
            'task',
            'module_complete',
        ]
        read_only_fields = ['training_plan', 'task', 'module_complete']


class ModuleSerializer(serializers.ModelSerializer):
    """serializer for the training plan module"""

    TaskSerializer = TaskRelationSerializer

    class Meta:
        """a class to specify the meta attribute"""

        model = Module
        fields = '__all__'
        read_only_fields = [
            'training_plan',
        ]
