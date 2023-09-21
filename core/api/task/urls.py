"""Url routes for task url view"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.task.viewset import (
    TaskViewSet,
    TaskCompletionViewSet,
    TaskCompletionViewSet,
)


router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'trainingplan/(?P<id>\d+)/module/(?P<module_id>\d+)/task', TaskViewSet)
router.register(
    r'trainingplan/(?P<id>\d+)/task/(?P<task_id>\d+)/completion',
    TaskCompletionViewSet,
)

urlpatterns = [path('', include(router.urls))]
