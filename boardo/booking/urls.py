from django.urls import path

from .views import *


urlpatterns = [

    path("add_category/",add_category,name="add_category"),
    path("add_vehicle/",add_vehicle,name="add_vehicle"),
    path("edit_vehicle/<int:vehicle_id>/",edit_vehicle,name="edit_vehicle"),
    path("delete_vehicle/<int:vehicle_id>/",delete_vehicle,name="delete_vehicle"),
    path("add_trip/",add_trip,name="add_trip",),
    path("edit_trip/<int:trip_id>/",edit_trip,name="edit_trip"),
    path("delete_trip/<int:trip_id>/",delete_trip,name="delete_trip"),
    path("add_stop/<int:trip_id>/",add_stop,name="add_stop"),
    path("book_trip/<int:trip_id>/",book_trip,name="book_trip"),
    path("seat_selection/<int:trip_id>/",seat_selection,name="seat_selection"),
    path("create_booking/<int:trip_id>/",create_booking,name="create_booking"),
    path("booking_success/<int:id>/",booking_success,name="booking_success"),
    path("agency_report/",agency_report,name="agency_report"),
    path("traveller_selection/<int:trip_id>/",traveller_selection,name="traveller_selection"),

]


