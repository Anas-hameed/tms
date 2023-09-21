"""Url routes for module API view"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.module.viewset import ModuleViewSet, ModuleCompletionViewSet


router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'trainingplan/(?P<id>\d+)/module', ModuleViewSet)
router.register(
    r'trainingplan/(?P<id>\d+)/module/(?P<module_id>\d+)/completion',
    ModuleCompletionViewSet,
)


urlpatterns = [
    path('', include(router.urls)),
]
