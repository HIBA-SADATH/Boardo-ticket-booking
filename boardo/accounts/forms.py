from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role"]
        widgets = {
            "role": forms.Select(
                attrs={
                    "class":"form-control"
                }
            )
        }


class AgencyRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "profile-input",
                    "placeholder": "Enter first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "profile-input",
                    "placeholder": "Enter last name",
                }
            ),

        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "image",
        ]
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "profile-input",
                    "placeholder": "Enter phone number",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "profile-input",
                    "accept": "image/*",
                }
            ),

        }


class TravellerForm(forms.ModelForm):
    class Meta:
        model = MyTraveller
        fields = [
            "full_name",
            "age",
            "gender",
            "phone",
            "email",
            "id_proof",
            "id_number",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter full name"
                }
            ),
            "age": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Age",
                    "min": 1
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address"
                }
            ),
            "id_proof": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Aadhaar / Passport / Driving Licence"
                }
            ),
            "id_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ID Number"
                }
            ),

        }
        labels = {
            "full_name": "Full Name",
            "age": "Age",
            "gender": "Gender",
            "phone": "Phone Number",
            "email": "Email Address",
            "id_proof": "ID Proof",
            "id_number": "ID Number",
        }



class TicketForm(forms.ModelForm):
    class Meta:
        model=SupportTicket

        fields=["subject","message"]
        widgets={

            "subject":forms.TextInput(attrs={"class":"form-control"}),

            "message":forms.Textarea(attrs={"class":"form-control","rows":5})
        }