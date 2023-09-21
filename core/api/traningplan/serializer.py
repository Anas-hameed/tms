"""Serializer class to convert json data for training plan"""

from rest_framework import serializers

from core.models import TrainingPlan, Invite
from core.api.user.serializer import UserRelationSerializer
from core.api.module.serializer import ModuleSerializer


class TrainingPlanSerializer(serializers.ModelSerializer):
    """a serializer for the training plan model"""

    class Meta:
        """a class to specify the meta parameter"""

        model = TrainingPlan
        fields = [
            'id',
            'name',
            'description',
            'create_date',
            'update_date',
            'duration',
            'creater',
        ]
        read_only_fields = ['creater']


class TrainingPlanModuleSerializer(serializers.ModelSerializer):
    """a serializer for the training plan model"""

    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        """a class to specify the meta parameter"""

        model = TrainingPlan
        fields = [
            'id',
            'name',
            'description',
            'create_date',
            'update_date',
            'duration',
            'creater',
            'modules',
        ]
        read_only_fields = ['creater', 'modules']


class InviteSerializer(serializers.ModelSerializer):
    """a serializer for the training plan model"""

    invitee = UserRelationSerializer(read_only=True)
    training_id = TrainingPlanSerializer(read_only=True)

    class Meta:
        """a class to specify the meta parameter"""

        model = Invite
        fields = [
            'id',
            'status',
            'email',
            'invite_date',
            'training_id',
            'invitee',
        ]
        read_only_fields = [
            'training_id',
            'inviter',
            'invitee',
        ]


class InviteListSerializer(serializers.ModelSerializer):
    """a serializer for the training plan model"""

    training_id = TrainingPlanSerializer(read_only=True)
    inviter = UserRelationSerializer(read_only=True)

    class Meta:
        """a class to specify the meta parameter"""

        model = Invite
        fields = [
            'id',
            'status',
            'email',
            'invite_date',
            'training_id',
            'inviter',
        ]
        read_only_fields = [
            'training_id',
            'inviter',
            'invitee',
        ]
