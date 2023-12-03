from django.core.management.base import BaseCommand
from ...models import Reservation, Room
from django.utils import timezone
from django.db.models import Q


class Command(BaseCommand):
    help = 'Updates room availability based on reservations'

    def handle(self, *args, **options):
        today = timezone.now().date()

        reservation_start = Reservation.objects.filter(start_date=today)

        for reservation in reservation_start:
            reservation.reserved_room.is_available=False
            reservation.reserved_room.save()
        
        reservation_end = Reservation.objects.filter(end_date=today)

        for reservation in reservation_end:
            reservation.reserved_room.is_available=True
            reservation.reserved_room.save()

        self.stdout.write(self.style.SUCCESS('Room availability updated successfully'))
