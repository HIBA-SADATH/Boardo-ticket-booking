from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from booking.models import Trip, Vehicle

from .forms import SearchForm, ReviewForm
from .models import (
    FavoriteTrip,
    Review,
    TravelHistory,
)


def search_trip(request):

    form = SearchForm(
        request.GET or None
    )

    trips = Trip.objects.none()

    source = ""
    destination = ""
    departure_date = None
    category = ""
    travellers = 1


    if form.is_valid():

        category = form.cleaned_data["category"]
        source = form.cleaned_data["source"]
        destination = form.cleaned_data["destination"]
        departure_date = form.cleaned_data["departure_date"]
        travellers = form.cleaned_data["travellers"]


        trips = (
            Trip.objects.filter(
                vehicle__category=category,
                source__icontains=source,
                destination__icontains=destination,
                departure_time__date=departure_date,
                status="scheduled",
            )
            .select_related(
                "vehicle"
            )
            .order_by(
                "departure_time"
            )
        )


    return render(
        request,
        "search_trip.html",
        {
            "form": form,
            "trips": trips,
            "source": source,
            "destination": destination,
            "departure_date": departure_date,
            "category": category,
            "travellers": travellers,
        }
    )



@login_required
def trip_detail(request, trip_id):

    trip = get_object_or_404(
        Trip.objects.select_related(
            "vehicle"
        ),
        id=trip_id
    )


    TravelHistory.objects.get_or_create(
        profile=request.user.profile,
        trip=trip,
    )


    return render(
        request,
        "trip_detail.html",
        {
            "trip": trip
        }
    )



@login_required
def add_favorite(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id
    )


    FavoriteTrip.objects.get_or_create(
        profile=request.user.profile,
        trip=trip,
    )


    return redirect(
        "trip_detail",
        trip_id=trip.id
    )



@login_required
def remove_favorite(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id
    )


    FavoriteTrip.objects.filter(
        profile=request.user.profile,
        trip=trip,
    ).delete()


    return redirect(
        "trip_detail",
        trip_id=trip.id
    )



@login_required
def add_review(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id
    )


    if request.method == "POST":

        form = ReviewForm(
            request.POST
        )


        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.profile = request.user.profile
            review.trip = trip

            review.save()


    return redirect(
        "trip_detail",
        trip_id=trip.id
    )



@login_required
def vehicle_list(request):

    vehicles = (
        Vehicle.objects.filter(
            agency=request.user.profile
        )
        .order_by(
            "-id"
        )
    )


    return render(
        request,
        "vehicle_list.html",
        {
            "vehicles": vehicles
        }
    )