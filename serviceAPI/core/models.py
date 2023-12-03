"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def upload_to(instance, filename):
    return f'images/{filename}'


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('user must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the systm."""
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserProfile(models.Model):
    """User profile."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True)
    name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    id_number = models.CharField(max_length=11, blank=True)


class Room(models.Model):
    """Room models."""
    CHOICES = (
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suit', 'Suit'),
    )
    room_number = models.CharField(max_length=10, blank=False, unique=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000, blank=True)
    type = models.CharField(max_length=8, choices=CHOICES, blank=False)
    bed_number = models.PositiveSmallIntegerField(blank=False ,default=1)
    room_size = models.IntegerField(blank=False)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(blank=False, max_digits=7, decimal_places=2)
    room_image1 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    room_image2 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    room_image3 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    room_image4 = models.ImageField(upload_to=upload_to, blank=True, null=True)


class Reservation(models.Model):
    """Reservation model."""
    reserved_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.SmallIntegerField(default=0)
    total_price = models.IntegerField()


