"""api defined view/controller for feedback"""

from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets

from core.api.feedback.serializer import FeedbackSerializer
from core.models import Feedback, Task
from core.api.permissions import IsOwner, IsEnrolledORCourseCreator


class FeedbackViewSet(viewsets.ModelViewSet):
    """Module for the Feedback viewset"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsEnrolledORCourseCreator,
        IsOwner,
    ]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    http_method_names = [
        'get',
        'post',
        'retrieve',
        'patch',
        'delete',
    ]

    def perform_create(self, serializer):
        """add the training plan while creating a module"""
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(task=task, user=self.request.user)
