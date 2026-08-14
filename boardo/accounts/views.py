from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from .models import Profile
from django.contrib.auth.decorators import login_required
from booking.models import Vehicle, Trip, Booking
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect,render
from accounts.forms import UserProfileForm, ProfileForm
from booking.models import Booking
from accounts.models import MyTraveller
from ollama import chat
from django.core.mail import send_mail

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            if user.is_superuser:
                return redirect("admindashboard")
            if user.profile.role == "agency":
                return redirect("agencydashboard")
            return redirect("home")

        messages.error(request,"Invalid username or password")
        return redirect(request.META.get("HTTP_REFERER","home"))
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                messages.error(
                    request,
                    "You are already registered. Please login."
                )
                return render(
                    request,
                    "register.html",
                    {"form": form}
                )
            user = form.save()
            login(request, user)
            send_mail(

                subject="Welcome to Boardo",

                message=f"""
                Hello {user.username},

                Welcome to Boardo!

                Your account has been created successfully.

                You can now book flights, trains, buses and events easily.

                Thank you for joining Boardo.

                Happy Travelling ✈️

                Team Boardo
                """,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,

            )
            messages.success(
                request,
                "Successfully registered. Welcome to Boardo!"
            )
            return redirect("home")
    else:
        form = RegisterForm()
    return render(
        request,
        "register.html",
        {"form": form}
    )


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def register_agency(request):
    if not request.user.is_superuser:
        return redirect("dashboard")
    form = AgencyRegisterForm()
    if request.method == "POST":
        form = AgencyRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            profile = user.profile
            profile.role = "agency"
            profile.save()
            return redirect("admindashboard")
    return render(request,"register_agency.html",{"form": form,},)


@login_required
def admin_reports(request):
    if not request.user.is_superuser:
        return redirect("dashboard")
    context = {
        "users": User.objects.filter(profile__role="user").count(),
        "agencies": User.objects.filter(profile__role="agency").count(),
        "vehicles": Vehicle.objects.count(),
        "trips": Trip.objects.count(),
        "bookings": Booking.objects.count(),
    }
    return render(request,"admin_reports.html",context)


@login_required
def admin_settings(request):
    if not request.user.is_superuser:
        return redirect("dashboard")
    return render(request,"admin_settings.html")




@login_required
def profile_view(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {"user_form": user_form,"profile_form": profile_form,"booking_count": Booking.objects.filter(profile=profile).count(),
        "traveller_count": MyTraveller.objects.filter(profile=profile).count()}

    return render(request, "profile.html", context)

@login_required
def traveller_list(request):
    travellers = MyTraveller.objects.filter(profile=request.user.profile).order_by("full_name")
    return render(request,"traveller_list.html",{"travellers": travellers})


@login_required
def add_traveller(request):
    if request.method == "POST":
        form = TravellerForm(request.POST)
        if form.is_valid():
            traveller = form.save(commit=False)
            traveller.profile = request.user.profile
            traveller.save()
            return redirect("traveller_list")
    else:
        form = TravellerForm()
    return render(
        request,
        "traveller_form.html",
        {"form": form,
          "title": "Add Traveller",
          "button": "Save Traveller",
        }
    )

@login_required
def edit_traveller(request, traveller_id):
    traveller = get_object_or_404(MyTraveller,id=traveller_id,profile=request.user.profile)
    if request.method == "POST":
        form = TravellerForm(request.POST,instance=traveller)
        if form.is_valid():
            form.save()
            return redirect("traveller_list")
    else:
        form = TravellerForm(instance=traveller)
    return render(
        request,
        "traveller_form.html",
        {
            "form": form,
            "title": "Edit Traveller",
            "button": "Update Traveller",
            "traveller": traveller,
        }
    )


@login_required
def delete_traveller(request, traveller_id):
    traveller = get_object_or_404(
        MyTraveller,
        id=traveller_id,
        profile=request.user.profile,
    )
    if request.method == "POST":
        traveller.delete()
        return redirect("traveller_list")
    return render(request,"delete_traveller.html",
        {
            "traveller": traveller,
        }
    )

def chatai(request):
    history = request.session.get("chat", [])
    if request.method == "POST":
        info = request.POST.get("data", "").strip()
        if info:
            history.append(
                {
                    "role": "user",
                    "content": info,
                }
            )
            response = chat(
                model="gemma3:4b",
                messages=history
            )
            raw_output = response["message"]["content"]
            history.append(
                {
                    "role": "assistant",
                    "content": raw_output,
                }
            )
            history = history[-6:]
            request.session["chat"] = history

    return render(
        request,
        "chatai.html",
        {
            "message": history
        }
    )



@login_required
def help_center(request):
    faqs = FAQ.objects.all()

    tickets = SupportTicket.objects.filter(
        profile=request.user.profile
    ).order_by("-created_at")

    form = TicketForm()

    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.profile = request.user.profile
            ticket.save()
            return redirect("help")

    context = {
        "faqs": faqs,
        "tickets": tickets,
        "form": form,
    }

    return render(request, "help.html", context)