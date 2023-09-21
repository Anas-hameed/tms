"""api defined view/controller for enrolment"""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, mixins, viewsets

from core.api.enrolment.serializer import (
    EnrolmentSerializer,
    EnrolmentUserSerializer,
)
from core.models import (
    Enrolment,
    Invite,
    TrainingPlan,
    User,
)
from core.api.permissions import IsCourseCreator, IsEnrolledORCourseCreator
from core.constants import TRAINER

class EnrolmentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Enrolment view for tranining plan registration"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class EnrolmentDetailViewSet(viewsets.ModelViewSet):
    """Enrolment view for tranining plan enrolment create, update, retrive and delete"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsCourseCreator,
    ]
    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer
    http_method_names = [
        'get',
        'post',
        'retrieve',
        'delete',
    ]

    def get_permissions(self):
        """return the permission for the methods"""
        if self.action in ['create', 'list']:
            return [
                permissions.IsAuthenticated(),
            ]
        if self.action == 'retrieve':
            return [
                permissions.IsAuthenticated(),
                IsEnrolledORCourseCreator(),
            ]
        return super().get_permissions()

    def get_queryset(self):
        """update the queryset method for list method"""
        if self.action == 'list':
            return super().get_queryset().filter(training_plan__creater=self.request.user)
        return super().get_queryset()
    
    def get_serializer(self, *args, **kwargs):
        """update the serializer class for the method"""
        if self.action == 'list':
            self.serializer_class = EnrolmentUserSerializer
        if self.action == 'retrieve' and self.request.user.role == TRAINER:
            self.serializer_class = EnrolmentUserSerializer
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        """perform create form the validated data"""
        return serializer.save(
            user=self.request.user, training_plan=self.request.training_plan
        )

    def create(self, request, *arg, **kwargs):
        """create the user enrolment for a course"""
        training_id = kwargs.get('id')
        request.training_plan = get_object_or_404(TrainingPlan, id=training_id)
        invite = get_object_or_404(
            Invite, training_id__id=training_id, invitee=request.user
        )
        invite.delete()
        return super().create(request, *arg, **kwargs)
