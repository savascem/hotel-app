"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(tags=['User app => Create a new user in the system.'])
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


@extend_schema(tags=['User app => Create a new auth token for user.'])
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES


@extend_schema(tags=['User app => Manage the auth user.'], description='text')
class MenageUserView(generics.RetrieveUpdateAPIView):
    """Manege the auth user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the auth user."""
        return self.request.user