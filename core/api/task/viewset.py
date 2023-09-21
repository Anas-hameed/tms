'api defined view/controller for task'

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from core.api.task.serializer import (
    TaskSerializer,
    TaskFeedbackSerializer,
    TaskCompletionSerializer,
)
from core.models import Module, Task, TaskCompletion
from core.api.permissions import (
    IsCourseCreator,
    IsEnrolledORCourseCreator,
    IsEnrolled,
    IsOwner,
)


class TaskViewSet(viewsets.ModelViewSet):
    """task for the module plan"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsCourseCreator,
    ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        """update the permission based on the action type"""
        if self.action in ['list', 'retrieve']:
            return [
                permissions.IsAuthenticated(),
                IsEnrolledORCourseCreator(),
            ]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        """update the serializer for the retrieve endpoint"""
        if self.action == 'retrieve':
            self.serializer_class = TaskFeedbackSerializer
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        """update the queryset based and apply the filter"""
        module_id = self.kwargs.get('module_id')
        return self.queryset.filter(module__id=module_id)

    def perform_create(self, serializer):
        """add the training plan while creating a module"""
        module = get_object_or_404(Module, id=self.kwargs.get('module_id'))
        serializer.save(module=module)


class TaskCompletionViewSet(viewsets.ModelViewSet):
    """provides route for the completion of the task"""

    permission_classes = [permissions.IsAuthenticated, IsEnrolled, IsOwner]
    queryset = TaskCompletion.objects.all()
    serializer_class = TaskCompletionSerializer
    http_method_names = ['list', 'get', 'post', 'retrieve', 'patch']

    def perform_create(self, serializer):
        """add the training plan while creating a module"""
        serializer.save(task=self.request.task, user=self.request.user)

    def list(self, request, *args, **kwargs):
        """update the queryset to contain only user specific completion"""
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = Task.objects.filter(id=task_id)
        if not task.exists():
            return Response(
                'no module exist with this id', status=status.HTTP_400_BAD_REQUEST
            )
        request.task = task[0]
        return super().create(request, *args, **kwargs)
