from django.db import models
from django.db import transaction

from accounts.models import MyTraveller, Profile


class Category(models.Model):
    CATEGORY_CHOICES = [
        ("flight", "Flight"),
        ("train", "Train"),
        ("bus", "Bus"),
        ("event", "Event"),
    ]
    type = models.CharField(max_length=20,choices=CATEGORY_CHOICES,unique=True,)

    class Meta:
        ordering = ["type"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.get_type_display()


class Agency(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name="agency")
    agency_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    logo = models.ImageField(upload_to="agency_logos/",blank=True,null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["agency_name"]

    def __str__(self):
        return self.agency_name


class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ("flight", "Flight"),
        ("train", "Train"),
        ("bus", "Bus"),
        ("event", "Event"),
    ]

    agency = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="vehicles",)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=50,unique=True,)
    logo = models.ImageField(upload_to="vehicle_logos/",blank=True,null=True,)
    total_seats = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["type", "name"]

    def __str__(self):
        return f"{self.type} - {self.vehicle_number}"


class Trip(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("boarding", "Boarding"),
        ("departed", "Departed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name="trips")
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    fare = models.DecimalField(max_digits=10,decimal_places=2)
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["departure_time"]

    @property
    def duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours and minutes:
            return f"{hours}h {minutes}m"
        if hours:
            return f"{hours}h"
        return f"{minutes}m"
    def __str__(self):
        return f"{self.source} → {self.destination}"

class Seat(models.Model):
    POSITION_CHOICES = [
        ("window", "Window"),
        ("middle", "Middle"),
        ("aisle", "Aisle"),
    ]
    DECK_CHOICES = [
        ("lower", "Lower"),
        ("upper", "Upper"),
    ]
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="seats")
    seat_number = models.CharField(max_length=10)
    position = models.CharField(max_length=20,choices=POSITION_CHOICES,default="window")
    deck = models.CharField(max_length=20,choices=DECK_CHOICES,default="lower")

    class Meta:
        ordering = ["seat_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "seat_number"],
                name="unique_trip_seat_number",
            )
        ]
    def __str__(self):
        return self.seat_number
class Booking(models.Model):

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    ]

    BOOKING_STATUS = [
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="bookings")
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="bookings")
    travellers = models.ManyToManyField(MyTraveller,related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,)
    payment_order_id = models.CharField(max_length=100, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    payment_signature = models.CharField(max_length=255, blank=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default="Pending")
    status = models.CharField(max_length=20,choices=BOOKING_STATUS,default="confirmed")

    class Meta:
        ordering = ["-booking_date"]

    def __str__(self):
        return f"Booking #{self.pk}"

class BookingSeat(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="booking_seats")
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="booking_seats")
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE,related_name="booking_seats",)
    passenger_gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    traveller = models.ForeignKey(MyTraveller,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "seat"],
                name="unique_trip_seat",
            )
        ]

    def __str__(self):
        return f"{self.trip} - {self.seat}"


class Stop(models.Model):
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="stops",)
    stop_name = models.CharField(max_length=100)
    arrival_time = models.DateTimeField(blank=True,null=True)
    departure_time = models.DateTimeField(blank=True,null=True,)
    stop_order = models.PositiveIntegerField()
    distance_from_source = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    class Meta:
        ordering = ["stop_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "stop_order"],
                name="unique_trip_stop_order",
            )
        ]

    def __str__(self):
        return f"{self.stop_order}. {self.stop_name}"