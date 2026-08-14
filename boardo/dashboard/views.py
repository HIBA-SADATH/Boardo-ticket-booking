from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from accounts.models import Profile
from accounts.forms import RoleUpdateForm
from booking.models import Vehicle, Trip, Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from booking.models import Booking
from travel.forms import SearchForm 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.forms import UserProfileForm, ProfileForm
from accounts.models import Profile
from accounts.forms import AgencyRegisterForm
from accounts.models import Profile


def home(request):
    form = SearchForm(initial={"category": "flight"})
    return render(
        request,
        "dashboard.html",{"form": form})



@login_required
def dashboard(request):
    profile = request.user.profile
    bookings = Booking.objects.filter(profile=profile)
    total_spent = bookings.aggregate(total=Sum("total_amount"))["total"] or 0
    form = SearchForm(initial={"category": "flight"})
    context = {
        "form": form,
        "bookings": bookings,
        "booking_count": bookings.count(),
        "total_spent": total_spent,
    }

    return render(request,"dashboard.html",context)


@login_required
def agencydashboard(request):
    profile = request.user.profile
    if profile.role != "agency":
        return redirect("dashboard")
    vehicles = Vehicle.objects.filter(agency=profile)
    trips = Trip.objects.filter(vehicle__agency=profile)
    bookings = Booking.objects.filter(trip__vehicle__agency=profile)
    revenue = bookings.filter(status="Confirmed").aggregate(total=Sum("total_amount"))["total"] or 0


    context = {
        "profile": profile,
        "vehicles": vehicles,
        "trips": trips,
        "bookings": bookings,
        "revenue": revenue,
    }
    return render(request,"agencydashboard.html",context)


def admin_check(user):
    return user.is_superuser



@login_required
@user_passes_test(admin_check)
def admindashboard(request):
    profiles = Profile.objects.all()
    context = {
        "profiles": profiles,
        "total_users":
            profiles.filter(
                role="user"
            ).count(),
        "total_agencies":
            profiles.filter(
                role="agency"
            ).count(),
        "total_vehicles":
            Vehicle.objects.count(),
        "total_trips":
            Trip.objects.count(),
        "total_bookings":
            Booking.objects.count(),
        "total_revenue":
            Booking.objects.aggregate(
                Sum("total_amount")
            )["total_amount__sum"] or 0,
        "recent_bookings":
            Booking.objects.all()
            .order_by("-booking_date")[:10],

    }
    return render(request,"admindashboard.html",context)



@login_required
@user_passes_test(admin_check)
def update_role(request, id):
    profile = get_object_or_404(Profile,id=id)
    if request.method == "POST":
        form = RoleUpdateForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect("admindashboard")
    else:
        form = RoleUpdateForm(instance=profile)
    return render(request,"update_role.html",
        {
            "form": form,
            "profile": profile
        }
    )

def user_list(request):
    pass

@staff_member_required
def agency_list(request):
    agencies = Profile.objects.filter(role="agency").select_related("user").order_by("user__username")
    context = {"agencies": agencies}
    return render(request,"agency_list.html",context)






@staff_member_required
def delete_agency(request, agency_id):
    agency = get_object_or_404(
        Profile,
        id=agency_id,
        role="agency"
    )
    if request.method == "POST":
        user = agency.user
        agency.delete()     
        user.delete()        
        messages.success(request,"Agency deleted successfully.")
        return redirect("agency_list")

    return render(request,"delete_agency.html",{"agency": agency})


@login_required
def edit_agency(request, agency_id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    profile = get_object_or_404(
        Profile,
        id=agency_id,
        role="agency"
)
    user = profile.user
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        password = request.POST.get("password")
        if password:
            user.set_password(password)
        user.save()
        return redirect("agency_list")
    context = {"agency": profile,}
    return render(request,"edit_agency.html",context,)



@login_required
def booking_list(request):
    bookings = Booking.objects.filter(profile=request.user.profile).order_by("-booking_date")
    context = {
        "bookings": bookings,
    }
    return render(request,"booking_list.html",context)

def category_list(request):
    pass

def reports(request):
    pass

def settings(request):
    return render(request,'admin_settings.html')

