from django import forms

from .models import Category, Stop, Trip, Vehicle


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["type"]
        widgets = {
            "type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "category",
            "name",
            "type",
            "model",
            "vehicle_number",
            "logo",
            "total_seats",
        ]
        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vehicle name",
                }
            ),
            "company": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company",
                }
            ),
            "model": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Model",
                }
            ),
            "vehicle_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vehicle Number",
                }
            ),
            "total_seats": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            "vehicle",
            "source",
            "destination",
            "departure_time",
            "arrival_time",
            "duration",
            "fare",
            "status",
        ]

        widgets = {
            "vehicle": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "source": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Starting Point",
                }
            ),
            "destination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Destination",
                }
            ),
            "departure_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "arrival_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Duration (minutes)",
                    "min": 1,
                }
            ),
            "fare": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ticket Fare",
                    "min": 0,
                    "step": "0.01",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        departure = cleaned_data.get("departure_time")
        arrival = cleaned_data.get("arrival_time")

        if departure and arrival and arrival <= departure:
            raise forms.ValidationError(
                "Arrival time must be after departure time."
            )

        return cleaned_data


class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = [
            "stop_name",
            "arrival_time",
            "departure_time",
            "stop_order",
            "distance_from_source",
        ]

        widgets = {
            "stop_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Stop Name",
                }
            ),
            "arrival_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "departure_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "stop_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "distance_from_source": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Distance (km)",
                    "step": "0.1",
                    "min": 0,
                }
            ),
        }