"""Url routes for traning plan API view"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.traningplan.viewset import (
    TraningPlanViewSet,
    TrainingInviteViewSet,
    TrainingInviteList,
)


router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'invites', TrainingInviteList)
router.register(r'(?P<id>\d+)/invites', TrainingInviteViewSet)
router.register(r'', TraningPlanViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
