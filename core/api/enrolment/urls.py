"""Url routes for enrolment API view"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.enrolment.viewset import EnrolmentViewSet, EnrolmentDetailViewSet


router = DefaultRouter()
router.include_format_suffixes = False
router.register('training/enrolment', EnrolmentViewSet)
router.register(r'training/(?P<id>\d+)/enrolment', EnrolmentDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
