from django.urls import path
from django.urls import path
from .views import payment_page, payment_success

urlpatterns = [

    path(
        "<int:booking_id>/",
        payment_page,
        name="payment_page",
    ),

    path(
        "success/",
        payment_success,
        name="payment_success",
    ),

]