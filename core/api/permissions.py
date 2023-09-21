"""custom permission class for rest api"""

from django.shortcuts import get_object_or_404

from rest_framework import permissions

from core.models import TrainingPlan, Enrolment
from core.constants import TRAINER


class IsOwner(permissions.BasePermission):
    """Custom permission for readonly object"""

    def has_object_permission(self, request, view, obj):
        """default method override to check for user ownership"""
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return obj == request.user


class IsTrainer(permissions.BasePermission):
    """check wheather the user is a trainer or not"""

    def __init__(self):
        self.message = 'Not autohrized to perform this action'
        super().__init__()

    def has_permission(self, request, view):
        """validate the incoming request for trainer"""
        if request.user.role != TRAINER:
            return False
        return True


class IsSafeMethod(permissions.BasePermission):
    """don't allow delete, post, put method"""

    def has_object_permission(self, request, view, obj):
        """Don't alow delete on the object"""
        not_allowed_method = [
            'POST',
            'DELETE',
            'PUT',
        ]
        if request.method in not_allowed_method:
            return False
        
        return True


class IsCourseCreator(permissions.BasePermission):
    """Allow only the creator to access the values"""

    def has_permission(self, request, view):
        training_id = view.kwargs.get('id')
        if not training_id:
            training_id = view.kwargs.get('pk')
        traning_plan = get_object_or_404(TrainingPlan, id=training_id)
        request.traning_plan = traning_plan
        return traning_plan.creater == request.user


class IsEnrolled(permissions.BasePermission):
    """Allow only the creator to access the values"""

    def has_permission(self, request, view):
        training_id = view.kwargs.get('id')
        if not training_id:
            training_id = view.kwargs.get('pk')
        traning_plan = Enrolment.objects.filter(
            training_plan__id=training_id,
            user=request.user,
        )
        if not traning_plan.exists():
            return False
        request.traning_plan = traning_plan
        return True


class IsEnrolledORCourseCreator(permissions.BasePermission):
    """check wheather a user is Enrolled or the course creator"""

    def has_permission(self, request, view):
        """check for the permissin and return True or false"""
        is_enrolled = IsEnrolled().has_permission(request, view)
        is_creator = IsCourseCreator().has_permission(request, view)
        return is_enrolled or is_creator
