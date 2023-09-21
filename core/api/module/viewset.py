"""api defined view/controller for module"""


from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from core.models import Module, ModuleCompletion
from core.api.module.serializer import (
    ModuleTaskSerializer,
    ModuleCompletionSerializer,
)
from core.api.permissions import (
    IsCourseCreator,
    IsEnrolledORCourseCreator,
    IsEnrolled,
    IsOwner,
)


class ModuleViewSet(viewsets.ModelViewSet):
    """Module for the training plan"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsCourseCreator,
    ]
    queryset = Module.objects.all()
    serializer_class = ModuleTaskSerializer

    def get_permissions(self):
        """update the permission based on the action type"""
        if self.action in ['list', 'retrieve']:
            return [
                permissions.IsAuthenticated(),
                IsEnrolledORCourseCreator(),
            ]
        return super().get_permissions()

    def get_queryset(self):
        """update the queryset based and apply the filter"""
        training_id = self.kwargs.get('id')
        return self.queryset.filter(training_plan__id=training_id)

    def perform_create(self, serializer):
        """add the training plan while creating a module"""
        serializer.save(training_plan=self.request.traning_plan)


class ModuleCompletionViewSet(viewsets.ModelViewSet):
    """provides route for the completion of the viewset"""

    permission_classes = [permissions.IsAuthenticated, IsEnrolled, IsOwner]
    queryset = ModuleCompletion.objects.all()
    serializer_class = ModuleCompletionSerializer
    http_method_names = ['list', 'get', 'post', 'retrieve', 'patch']

    def perform_create(self, serializer):
        """add the training plan while creating a module"""
        serializer.save(module=self.request.module, user=self.request.user)

    def list(self, request, *args, **kwargs):
        """update the queryset to contain only user specific completion"""
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        module_id = kwargs.get('module_id')
        module = Module.objects.filter(id=module_id)
        if not module.exists():
            return Response(
                'no module exist with this id', status=status.HTTP_400_BAD_REQUEST
            )
        request.module = module[0]
        return super().create(request, *args, **kwargs)
