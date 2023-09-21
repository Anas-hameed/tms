"""Serializer class to convert the enrolment table to python native type"""

from rest_framework import serializers

from core.models import Enrolment
from core.api.traningplan.serializer import TrainingPlanSerializer
from core.api.user.serializer import UserRelationSerializer


class EnrolmentSerializer(serializers.ModelSerializer):
    """Enrolment serializer for enrolment of trainee to a training plan"""

    training_plan = TrainingPlanSerializer(read_only=True)
    user = UserRelationSerializer(read_only=True)

    class Meta:
        """a class to specify the meta parameter"""

        model = Enrolment
        fields = [
            'id',
            'user',
            'training_plan',
        ]
        read_only_fields = [
            'user',
            'training_plan',
            'user',
        ]


class EnrolmentUserSerializer(serializers.ModelSerializer):
    """Enrolment serializer for enrolment list method"""

    user = UserRelationSerializer(read_only=True)
    training_plan = TrainingPlanSerializer(read_only=True)

    class Meta:
        """a class to specify the meta parameter"""

        model = Enrolment
        fields = [
            'id',
            'user',
            'training_plan',
        ]
        read_only_fields = [
            'user',
            'training_plan',
        ]
