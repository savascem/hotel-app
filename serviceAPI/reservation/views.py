"""
Views for the reservation API.
"""
from core.models import Reservation
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from django.utils import timezone
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Reservation App => Enables to CRUD operations.'])
class ReservationViewSet(viewsets.ModelViewSet):
    """View set for reservation model. Supported create, retrieve, update, patch methods."""
    serializer_class = serializers.ReservationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    def list(self, request, *args, **kwargs):
        """Return reservations for user who requested."""
        queryset = Reservation.objects.filter(user=request.user)
        serializer = serializers.ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Destroys object which is specified."""
        instance = self.get_object()
        today = timezone.now().date()

        if instance.start_date < today:
            return Response("You cannot delete old reservations.", status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Reservation App => APIView to retrieve a list of reservations that entered room ID.'])
class RetrieveReservationListForRoomViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """APIView to retrieve a list of reservations that entered room ID."""
    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        """Retrieve method for RetrieveReservationListForRoomViewSet"""
        pk = self.kwargs['pk']
        queryset = Reservation.objects.filter(reserved_room=pk)
        serializer = serializers.ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


    
