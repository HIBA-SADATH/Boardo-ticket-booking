from django.urls import path

from .views import (
    add_favorite,
    add_review,
    remove_favorite,
    search_trip,
    trip_detail,
    vehicle_list,
)


urlpatterns = [

    path(
        "search/",
        search_trip,
        name="search_trip",
    ),

    path(
        "trip/<int:trip_id>/",
        trip_detail,
        name="trip_detail",
    ),

    path(
        "favorite/<int:trip_id>/",
        add_favorite,
        name="add_favorite",
    ),

    path(
        "favorite/remove/<int:trip_id>/",
        remove_favorite,
        name="remove_favorite",
    ),

    path(
        "review/<int:trip_id>/",
        add_review,
        name="add_review",
    ),

    path(
        "vehicles/",
        vehicle_list,
        name="vehiclelist",
    ),

]