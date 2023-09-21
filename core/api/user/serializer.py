"""Serializer class to convert to json data for user"""

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.models import User, UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    'serializer for Profile'

    class Meta:
        """profile serilizer properties to displayed"""

        model = UserProfile
        fields = ['id', 'gender', 'bio', 'profile_image', 'user']
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user"""

    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        """meta properties to be serialized for user"""

        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'password',
            'profile',
        ]
        read_only_fields = ['profile']


class UserRelationSerializer(serializers.ModelSerializer):
    """Serializer for user"""

    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        """meta properties to be serialized for user"""

        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile',
        ]
        read_only_fields = ['profile']


class ForgetPasswordSerializer(serializers.Serializer):
    """difinition of the forget password serializer"""

    email = serializers.EmailField()

    def validate_email(self, value):
        """Validate that the provided email exists in the system"""
        user = User.objects.filter(email=value)
        if not user.exists():
            raise serializers.ValidationError('Email does not exist in our system.')
        self.user = user[0]
        return value


class ResetForgetPasswordSerializer(serializers.Serializer):
    """reset the user password for the email"""

    email = serializers.EmailField()
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """validate the data and return the validate data"""
        token_key = data.get('token')
        password = data.get('password')
        token = ''
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise serializers.ValidationError('Invalid token provided')
        user = token.user
        token.delete()
        password = make_password(password)
        user.password = password
        user.save()
        new_token = Token.objects.create(user=user)
        self.new_token = new_token
        return data


class MapUserSerializer(serializers.Serializer):
    """value for the serializer"""

    email = serializers.EmailField()
    given_name = serializers.CharField(max_length=30)
    family_name = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=60)