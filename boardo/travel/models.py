from django.db import models
from accounts.models import Profile
from booking.models import Trip


class TravelHistory(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="travel_history")
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="view_history")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            "-viewed_at"]
        indexes = [
            models.Index(
                fields=[
                    "profile",
                    "viewed_at"
                ]
            )
        ]

    def __str__(self):
        return (
            f"{self.profile.user.username} "
            f"viewed {self.trip}"
        )



class FavoriteTrip(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="favorite_trips"
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "profile",
                    "trip"
                ],
                name="unique_favorite_trip"
            )
        ]

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return (
            f"{self.profile.user.username} - "
            f"{self.trip}"
        )



class Review(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True
    )

    rating = models.PositiveIntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ]
    )

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return (
            f"{self.rating}/5 - "
            f"{self.profile.user.username}"
        )