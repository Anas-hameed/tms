"""Url routes for user API view"""

from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from core.api.user.viewset import (
    CurrentUserView,
    UserList,
    UserDetails,
    ProfileViewsSet,
    ForgetPasswordView,
    ForgetPasswordResetView,
    MapGoogleUserView
)


router = DefaultRouter()
router.include_format_suffixes = False
router.register('profile', ProfileViewsSet)

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('', UserList.as_view()),
    path('<int:pk>/', UserDetails.as_view()),
    path('', include(router.urls)),
    path('me/', CurrentUserView.as_view()),
    path('reset_password/', ForgetPasswordView.as_view()),
    path('password/reset/', ForgetPasswordResetView.as_view()),
    path('google/oauth/', MapGoogleUserView.as_view()),
]

urlpatterns += [
    path('login/', include('rest_framework.urls')),
]
