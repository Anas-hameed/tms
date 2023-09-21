"""api defined view/controller for trainingplan and trainingplan invite"""

from rest_framework import permissions, mixins, viewsets, status
from rest_framework.response import Response

from core.api.traningplan.serializer import (
    TrainingPlanSerializer,
    TrainingPlanModuleSerializer,
    InviteSerializer,
    InviteListSerializer,
)
from core.models import User, TrainingPlan, Invite
from core.api.permissions import IsTrainer, IsCourseCreator, IsEnrolledORCourseCreator
from core.helpers.send_email import send_invite_email


class TraningPlanViewSet(viewsets.ModelViewSet):
    """A course viewset for the course class"""

    serializer_class = TrainingPlanModuleSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsCourseCreator,
    ]

    def get_permissions(self):
        """update the permission value for the retrieve"""
        if self.action == 'retrieve':
            return [
                permissions.IsAuthenticated(),
                IsEnrolledORCourseCreator(),
            ]
        if self.action in ['list', 'create']:
            return [
                permissions.IsAuthenticated(),
                IsTrainer(),
            ]
        return super().get_permissions()

    def perform_create(self, serializer):
        """add the current user while creating the course"""
        serializer.save(creater=self.request.user)

    def list(self, request, *args, **kwargs):
        """filter the queryset to return course or user enrolled course"""
        self.queryset = self.queryset.filter(creater=request.user)
        self.serializer_class = TrainingPlanSerializer
        return super().list(request, *args, **kwargs)


class TrainingInviteList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """invite the user to the traning plan"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = InviteListSerializer
    queryset = Invite.objects.all()

    def get_queryset(self):
        """update the queryset for the user"""
        return super().get_queryset().filter(email=self.request.user.email)


class TrainingInviteViewSet(viewsets.ModelViewSet):
    """Invite details viewset to retrive, destory, and update invite"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsCourseCreator,
    ]
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer

    http_method_names = [
        'get',
        'post',
        'retrieve',
        'patch',
        'delete',
    ]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """update the queryset for the user"""
        if self.action == 'list':
            return super().get_queryset().filter(inviter=self.request.user)
        return self.queryset

    def list(self, request, id=None):
        """return the list of invite of the particular course"""
        serializer = InviteSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, id=None):
        """create an invite for the user"""
        serializer = InviteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        training = request.traning_plan
        if self.queryset.filter(training_id=request.traning_plan, email=email).exists():
            return Response(
                {'err': 'user invite exist for the course'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_invite_email(
            request.traning_plan.id,
            request.traning_plan.name,
            email,
        )
        user = User.objects.filter(email=email)
        if user.exists():
            serializer.save(training_id=training, inviter=request.user, invitee=user[0])
        else:
            serializer.save(training_id=training, inviter=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
