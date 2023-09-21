"""Url routes for feedback API view"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.feedback.viewset import FeedbackViewSet


router = DefaultRouter()
router.include_format_suffixes = False
router.register(
    r'trainingplan/(?P<id>\d+)/task/(?P<task_id>\d+)/feedback', FeedbackViewSet
)

urlpatterns = [
    path('', include(router.urls)),
]
