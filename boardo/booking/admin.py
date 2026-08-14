from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Vehicle)
admin.site.register(Trip)
admin.site.register(Stop)
admin.site.register(Booking)