from django.contrib import admin
from accounts.models import Profile, MyTraveller
from .models import *

class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "phone",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "user__username",
        "user__email",
    )




class MyTravellerAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "profile",
        "age",
        "gender",
    )

    list_filter = (
        "gender",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
    )

# Register your models here.
