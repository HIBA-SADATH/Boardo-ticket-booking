from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .forms import CategoryForm, TripForm ,StopForm, VehicleForm
from .models import *
from accounts.models import MyTraveller
from travel.models import Review
import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)

@login_required
def add_category(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category added successfully.")
        return redirect("agencydashboard")
    return render(request,"add_category.html",{"form": form,},)


@login_required
def add_vehicle(request):
    form = VehicleForm(
        request.POST or None,
        request.FILES or None,
    )
    if request.method == "POST" and form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.agency = request.user.profile
        vehicle.save()
        messages.success(request,"Vehicle added successfully.")
        return redirect("agencydashboard")

    return render(request,"add_vehicle.html",{"form": form})


@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle,id=vehicle_id,agency=request.user.profile)
    form = VehicleForm(request.POST or None,request.FILES or None,instance=vehicle,)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request,"Vehicle updated successfully.")
        return redirect("agencydashboard")
    return render(request,"edit_vehicle.html",{"vehicle": vehicle,"form": form})


@login_required
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle,id=vehicle_id,agency=request.user.profile)
    if request.method == "POST":
        vehicle.delete()
        messages.success(request,"Vehicle deleted successfully.")
        return redirect("agencydashboard")
    return render(request,"delete_vehicle.html",{"vehicle": vehicle})

@login_required
def add_trip(request):
    form = TripForm(request.POST or None)
    form.fields["vehicle"].queryset = Vehicle.objects.filter(agency=request.user.profile)
    if request.method == "POST" and form.is_valid():
        trip = form.save(commit=False)
        trip.available_seats = trip.vehicle.total_seats
        trip.save()
        category = trip.vehicle.category
        if category in ["bus", "flight"]:
            seats = []
            for i in range(1, trip.vehicle.total_seats + 1):
                if category == "flight":
                    if i % 3 == 1:
                        position = "window"
                    elif i % 3 == 2:
                        position = "middle"
                    else:
                        position = "aisle"
                else:
                    position = "window" if i % 2 == 0 else "aisle"
                seats.append(Seat(trip=trip,seat_number=f"S{i}",position=position))
            Seat.objects.bulk_create(seats)

        messages.success(request,"Trip added successfully.")
        return redirect("agencydashboard")

    return render(request,"add_trip.html",{"form": form})


@login_required
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip,id=trip_id,vehicle__agency=request.user.profile,)
    form = TripForm(request.POST or None,instance=trip)
    form.fields["vehicle"].queryset = Vehicle.objects.filter(agency=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request,"Trip updated successfully.")
        return redirect("agencydashboard")
    return render(request,"edit_trip.html",
        {
            "trip": trip,
            "form": form,
        },
    )


@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip,id=trip_id,vehicle__agency=request.user.profile,)
    if request.method == "POST":
        trip.delete()
        messages.success(request,"Trip deleted successfully.")
        return redirect("agencydashboard")
    return render(request,"delete_trip.html",
        {
            "trip": trip,
        },
    )


@login_required
def add_stop(request, trip_id):
    trip = get_object_or_404(Trip,id=trip_id,vehicle__agency=request.user.profile,)
    form = StopForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        stop = form.save(commit=False)
        stop.trip = trip
        stop.save()
        messages.success(request,"Stop added successfully.")
        return redirect("agencydashboard")
    return render(request,"add_stop.html",
        {
            "trip": trip,
            "form": form,
        },
    )

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip.objects.select_related("vehicle"),id=trip_id,)
    seats = Seat.objects.filter(trip=trip).order_by("seat_number")
    booked_seat_ids = set(BookingSeat.objects.filter(
            trip=trip
        ).values_list(
            "seat_id",
            flat=True,
        )
    )

    return render(request,"book_trip.html",
        {
            "trip": trip,
            "seats": seats,
            "booked_seat_ids": booked_seat_ids,
        },
    )


@login_required
def seat_selection(request, trip_id):
    trip = get_object_or_404(
        Trip.objects.select_related("vehicle"),
        id=trip_id,
    )
    seats = Seat.objects.filter(trip=trip
    ).order_by("seat_number")
    booked_seat_ids = set(BookingSeat.objects.filter(trip=trip).values_list("seat_id",flat=True,))
    return render(request,"seat_selection.html",
        {
            "trip": trip,
            "seats": seats,
            "booked_seat_ids": booked_seat_ids,
        },
    )

@login_required
@transaction.atomic
def create_booking(request, trip_id):
    if request.method != "POST":
        return redirect(
            "book_trip",
            trip_id=trip_id )
    trip = get_object_or_404(Trip.objects.select_for_update(),id=trip_id)
    selected_data = request.POST.get("selected_seats","",)
    selected_ids = [
        int(i)
        for i in selected_data.split(",")
        if i.strip()
    ]
    if not selected_ids:
        messages.error(
            request,
            "Please select at least one seat.",
        )
        return redirect("book_trip",trip_id=trip.id,)

    seats = Seat.objects.filter(trip=trip,id__in=selected_ids)
    if seats.count() != len(selected_ids):
        messages.error(request,"Invalid seat selection.")
        return redirect("book_trip", trip_id=trip.id)
    if BookingSeat.objects.filter(trip=trip,seat__in=seats).exists():
        messages.error(request,"One or more seats are already booked.",)
        return redirect("book_trip",trip_id=trip.id)
    if trip.available_seats < seats.count():
        messages.error(request,"Not enough seats available.",)
        return redirect("book_trip",trip_id=trip.id,)
    booking = Booking.objects.create(profile=request.user.profile,trip=trip,total_amount=trip.fare * seats.count())
    amount = int(booking.total_amount * 100)
    order = client.order.create(
        {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,
        }
    )
    booking.payment_order_id = order["id"]
    booking.save(update_fields=["payment_order_id"])
    traveller_ids = []
    booking_seats = []
    for seat in seats:
        traveller_id = request.POST.get(
            f"traveller_for_{seat.id}")
        if not traveller_id:
            messages.error(request,f"Please select a traveller for Seat {seat.seat_number}.")
            return redirect("traveller_selection",trip_id=trip.id,)
        traveller = get_object_or_404(MyTraveller,id=traveller_id,profile=request.user.profile)
        traveller_ids.append(traveller.id)
        booking_seats.append(
            BookingSeat(
                booking=booking,
                trip=trip,
                seat=seat,
                traveller=traveller,
                passenger_gender=traveller.gender,
            )

        )
    booking.travellers.set(traveller_ids)
    BookingSeat.objects.bulk_create(booking_seats)
    return redirect("payment_page",booking_id=booking.id)

@login_required
def booking_success(request, id):
    booking = get_object_or_404(Booking.objects.select_related("trip","profile"),id=id,profile=request.user.profile)
    selected_seats = list(booking.booking_seats.values_list( "seat__seat_number",flat=True ))
    return render(request,"booking_success.html",{
            "booking": booking,
            "selected_seats": selected_seats,
        } )


@login_required
def agency_report(request):
    agency = request.user.profile
    trips = (Trip.objects.filter(vehicle__agency=agency)
        .select_related("vehicle")
        .prefetch_related("bookings")
    )
    bookings = Booking.objects.filter(trip__vehicle__agency=agency).select_related("trip","profile", )
    total_trips = trips.count()
    total_bookings = bookings.count()
    total_revenue = (bookings.aggregate(total=Sum("total_amount")["total"] or 0))
    available_seats = (trips.aggregate(total=Sum("available_seats"))["total"] or 0)
    seats_sold = BookingSeat.objects.filter(trip__vehicle__agency=agency).count()
    popular_trips = (trips.annotate(booking_count=Count("bookings")).order_by("-booking_count")[:5])
    recent_bookings = bookings.order_by("-booking_date")[:10]
    reviews = (Review.objects.filter(trip__vehicle__agency=agency)
        .select_related(
            "trip",
            "user",
        )
        .order_by("-created_at")[:10]
    )

    context = {
        "total_trips": total_trips,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "available_seats": available_seats,
        "seats_sold": seats_sold,
        "popular_trips": popular_trips,
        "recent_bookings": recent_bookings,
        "reviews": reviews,
    }

    return render(request,"agency_report.html",context,)


def is_admin(user):
    return (
        user.is_authenticated
        and user.is_superuser
    )


def is_agency(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "agency"
    )


def is_user(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "user"
    )

@login_required
def traveller_selection(request, trip_id):
    trip = get_object_or_404(
        Trip,
        id=trip_id,
    )
    selected_seats = request.GET.get("seats", "")
    seat_ids = [
        int(i)
        for i in selected_seats.split(",")
        if i.strip()
    ]
    seats = Seat.objects.filter(
        id__in=seat_ids,
        trip=trip,
    )
    travellers = MyTraveller.objects.filter(
        profile=request.user.profile
    ).order_by("full_name")
    return render(request,"traveller_selection.html",
        {
            "trip": trip,
            "seats": seats,
            "selected_seats": selected_seats,
            "travellers": travellers,
        },
    )