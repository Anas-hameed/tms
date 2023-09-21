"""api defined view/controller for user routes"""

from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from core.api.user.serializer import (
    UserSerializer,
    ProfileSerializer,
    ForgetPasswordSerializer,
    ResetForgetPasswordSerializer,
    MapUserSerializer,
)
from core.models import User, UserProfile
from core.api.permissions import IsOwner, IsSafeMethod
from core.helpers.send_email import forget_password_email


class UserList(generics.CreateAPIView):
    """return a list of users, create a user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """update the create method to save a hash instead of pure password"""

        password = make_password(self.request.data['password'])
        serializer.save(password=password)


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    """details view for the user api, update or delete user"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        """override put to allow partial update on user"""
        return self.partial_update(request, *args, **kwargs)


class ProfileViewsSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """provide  retrive and update functionality on Profile viewset"""

    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
        IsSafeMethod,
    ]


class CurrentUserView(APIView):
    """validate the request and return the user based on authentication type"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        """return the current user"""
        user = UserSerializer(request.user)
        return Response(user.data)


class MapGoogleUserView(APIView):
    """This class map the google user with django user"""

    def post(self, request):
        """handle the post request to create a new user or return token"""
        serializer = MapUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = serializer.validated_data['name']
            user.first_name = serializer.validated_data['given_name']
            user.last_name = serializer.validated_data['family_name']
            user.set_password(f"{serializer.validated_data['name']}_{email}")
            user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user)
        return Response(
            {
                'message': 'User mapping successful',
                'token': token.key,
                'user':user_data.data
            },
            status=status.HTTP_201_CREATED,
        )


class ForgetPasswordView(APIView):
    """handle route for user forget password"""

    def post(self, request):
        """send an email to the given email for password reset"""
        serializer = ForgetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        forget_password_email(serializer.user)
        return Response(
            'forget password link is send to you email',
            status=status.HTTP_200_OK,
        )


class ForgetPasswordResetView(APIView):
    """This route for forget password from a post request with token"""

    def post(self, request):
        """post method to handle reset password"""
        serializer = ResetForgetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                'message': 'password reset was sucessful',
                'token': serializer.new_token.key,
            },
            status=status.HTTP_200_OK,
        )
