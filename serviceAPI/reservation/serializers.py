"""
Serializers for the user API.
"""
from rest_framework import serializers
from django.db.models import Q
from django.utils import timezone

from core.models import (
    Reservation, Room,
)


def get_days_interval_and_total_price(end_date, start_date, reserved_room_id):
    """Calculate and return values for days, total_price fields."""
    days = (end_date - start_date).days - 1
    room = Room.objects.get(id=reserved_room_id)
    total_price = days * room.price

    return days, total_price

class ReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'days', 'total_price', 'reserved_room']
        read_only_fields = ['days', 'total_price']

    def validate(self, data):
        """Validete datas which are coming with serializer."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        reserved_room = data.get('reserved_room')

        if not reserved_room:
            raise serializers.ValidationError("Room number must be specify.")

        if not (start_date and end_date):
            raise serializers.ValidationError("Check-out date and check-in date must be specify.")
        
        if start_date >= end_date:
            raise serializers.ValidationError("Check-out date must be later than check-in date.")
        
        if start_date < timezone.now().date():
            raise serializers.ValidationError("The check-in date cannot be older than today.")
        
        return data
        
    def create(self, validated_data):
        """Validates and create new object which is coming with post request."""
        user = self.context['request'].user
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        reserved_room = validated_data['reserved_room']

        scnerio1_1 = Reservation.objects.filter(Q(user=user) & Q(start_date__gte=start_date) & Q(end_date__gte=end_date) & Q(start_date__lt=end_date)).exists()
        scnerio1_2 = Reservation.objects.filter(Q(user=user) & Q(start_date__lte=start_date) & Q(end_date__lte=end_date) & Q(end_date__gt=start_date)).exists()
        scnerio1_3 = Reservation.objects.filter(Q(user=user) & Q(start_date__lte=start_date) & Q(end_date__gte=end_date)).exists()

        if scnerio1_1 or scnerio1_2 or scnerio1_3:
            """Generates error ,if user have already any reservation in selected days"""
            raise serializers.ValidationError("You already have a reservation for selected days.")
        
        scnerio2_1 = Reservation.objects.filter(Q(reserved_room=reserved_room)  & Q(start_date__gte=start_date) & Q(end_date__gte=end_date) & Q(start_date__lt=end_date)).exists()
        scnerio2_2 = Reservation.objects.filter(Q(reserved_room=reserved_room) & Q(start_date__lte=start_date) & Q(end_date__lte=end_date) & Q(end_date__gt=start_date)).exists()
        scnerio2_3 = Reservation.objects.filter(Q(reserved_room=reserved_room) & Q(start_date__lte=start_date) & Q(end_date__gte=end_date)).exists()

        if scnerio2_1 or scnerio2_2 or scnerio2_3:
            """Generates error ,if any reservation is already exist on the room in selected days"""
            raise serializers.ValidationError("This room is already booked for the days you have selected.")
        
        days, total_price = get_days_interval_and_total_price(end_date, start_date, reserved_room.id)

        return Reservation.objects.create(user=user, days=days, total_price=total_price, **validated_data)

    def update(self, instance, validated_data):
        """Validates and update object which is coming with put or patch request."""
        user = self.context['request'].user
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        reserved_room = validated_data['reserved_room']

        scenerio1_1 = Reservation.objects.filter(Q(reserved_room=reserved_room) & Q(start_date__gte=start_date) & Q (end_date__gte=end_date) & Q(start_date__lt=end_date)).exclude(user=user).exists()
        scenerio1_2 = Reservation.objects.filter(Q(reserved_room=reserved_room) & Q(start_date__lte=start_date) & Q (end_date__lte=end_date) & Q(end_date__gt=start_date)).exclude(user=user).exists()
        scenerio1_3 = Reservation.objects.filter(Q(reserved_room=reserved_room) & Q(start_date__lte=start_date) & Q (end_date__gte=end_date)).exclude(user__id=user.id).exists()

        if scenerio1_1 or scenerio1_2 or scenerio1_3:
            """Generates error ,if any reservation is already exist on the room in selected days"""
            raise serializers.ValidationError("This room is not available for these days.")
        
        days, total_price = get_days_interval_and_total_price(end_date, start_date, reserved_room.id)

        instance.start_date = start_date
        instance.end_date = end_date
        instance.reserved_room = reserved_room
        instance.days = days
        instance.total_price = total_price

        instance.save()

        return instance

