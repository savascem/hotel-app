"""
Views for the room API.
"""
from core.models import Room
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from drf_spectacular.utils import extend_schema


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to perform
    write operations (POST, PUT, DELETE), but allow anyone to
    perform read-only operations (GET).
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, and OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an admin.
        return request.user and request.user.is_staff


@extend_schema(tags=['Room App => API endpoints for Room model. Enables to Create, Update, Destroy operations only to Admins.'])
class RoomCreateUpdateDestroyViewSet(viewsets.ModelViewSet):
    """Viewset for Room model"""
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
        

@extend_schema(tags=['Room App => OnlyRead API endpoints for Room model. Enables to searching with title, decription and type.'])
class RoomOnlyReadViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Viewset for Room model"""
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """The queryset will provide searching."""
        query = self.request.query_params.get("q")
        if query:
            return Room.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(type__icontains=query)
            )
        else:
            return Room.objects.all()
