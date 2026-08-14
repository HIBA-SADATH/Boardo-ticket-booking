from datetime import date

from django import forms

from .models import Review


class SearchForm(forms.Form):

    category = forms.CharField(
        widget=forms.HiddenInput()
    )

    source = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter source"
            }
        )
    )

    destination = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter destination"
            }
        )
    )

    departure_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "min": date.today().strftime("%Y-%m-%d")
            }
        )
    )

    travellers = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter number of travellers"
            }
        )
    )


class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=[
            (5, "★★★★★"),
            (4, "★★★★"),
            (3, "★★★"),
            (2, "★★"),
            (1, "★"),
        ],
        widget=forms.RadioSelect,
        label="Rating"
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us about your journey...",
                "rows": 5
            }
        ),
        required=False,
        label="Your Review"
    )

    class Meta:
        model = Review

        fields = [
            "rating",
            "comment"
        ]