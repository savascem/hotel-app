"""
Serializers for the room API.
"""
from rest_framework import serializers

from core.models import (
    Room,
)


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""
    class Meta:
        model = Room
        fields = '__all__'
