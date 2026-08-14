from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

import razorpay

from booking.models import Booking, BookingSeat


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)


@login_required
def payment_page(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        profile=request.user.profile,
    )

    if not booking.payment_order_id:

        order = client.order.create(
            {
                "amount": int(booking.total_amount * 100),
                "currency": "INR",
                "payment_capture": 1,
            }
        )

        booking.payment_order_id = order["id"]
        booking.save(update_fields=["payment_order_id"])

    else:

        order = client.order.fetch(
            booking.payment_order_id
        )

    return render(
        request,
        "payment.html",
        {
            "booking": booking,
            "key": settings.RAZORPAY_KEY_ID,
            "amount": order["amount"],
        },
    )


@login_required
@transaction.atomic
def payment_success(request):

    payment_id = request.GET.get("payment_id")
    order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")

    booking = get_object_or_404(
        Booking.objects.select_for_update(),
        payment_order_id=order_id,
    )

    try:

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )

    except razorpay.errors.SignatureVerificationError:

        booking.payment_status = "Failed"
        booking.save(update_fields=["payment_status"])

        messages.error(
            request,
            "Payment verification failed."
        )

        return redirect(
            "payment_page",
            booking_id=booking.id,
        )

    if booking.payment_status == "Paid":

        messages.info(
            request,
            "Payment already completed."
        )

        return redirect(
            "booking_success",
            id=booking.id,
        )

    booking.payment_status = "Paid"
    booking.payment_id = payment_id
    booking.payment_signature = signature

    booking.save(
        update_fields=[
            "payment_status",
            "payment_id",
            "payment_signature",
        ]
    )

    trip = booking.trip

    seat_count = booking.booking_seats.count()

    trip.available_seats -= seat_count

    if trip.available_seats < 0:
        trip.available_seats = 0

    trip.save(update_fields=["available_seats"])

    messages.success(
        request,
        "Payment completed successfully!"
    )

    return redirect(
        "booking_success",
        id=booking.id,
    )