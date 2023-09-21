"""Serializer class to convert to json data for feedback"""

from rest_framework import serializers

from core.models import Feedback
from core.api.user.serializer import UserRelationSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    """serializer class for the task"""

    class Meta:
        """a class to specify the meta attribute"""

        model = Feedback
        fields = [
            'id',
            'message',
            'date',
            'user',
            'task',
        ]
        read_only_fields = [
            'user',
            'task',
        ]


class FeedbackUserSerializer(serializers.ModelSerializer):
    """serializer class for the task"""

    user = UserRelationSerializer(read_only=True)

    class Meta:
        """a class to specify the meta attribute"""

        model = Feedback
        fields = [
            'id',
            'message',
            'date',
            'user',
        ]
        read_only_fields = [
            'user',
        ]
