from .models import Seat


def generate_seats(trip):

    if Seat.objects.filter(trip=trip).exists():
        return


    seats = []


    for i in range(1, trip.total_seats + 1):

        seats.append(

            Seat(
                trip=trip,
                seat_number=f"S{i}"
            )

        )


    Seat.objects.bulk_create(seats)