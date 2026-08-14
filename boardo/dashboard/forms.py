from django import forms

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):

    class Meta:
        model = SiteSettings

        fields = [
            "website_name",
            "support_email",
            "support_phone",
            "logo",
            "maintenance_mode",
        ]

        widgets = {

            "website_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Website Name",
                }
            ),

            "support_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Support Email",
                }
            ),

            "support_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Support Phone",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "maintenance_mode": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }