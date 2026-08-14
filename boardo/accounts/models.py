from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("agency", "Agency"),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile",)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="user",)
    phone = models.CharField(max_length=15,blank=True,null=True,)
    image = models.ImageField(upload_to="profile/",blank=True,null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username


class MyTraveller(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="travellers")
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15,blank=True,null=True,)
    email = models.EmailField(blank=True,null=True)
    id_proof = models.CharField(max_length=30,blank=True,help_text="Aadhaar, Passport, Driving Licence, Voter ID, etc.",)
    id_number = models.CharField(max_length=50,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Traveller"
        verbose_name_plural = "Travellers"

    def __str__(self):
        return f"{self.full_name} ({self.profile.user.username})"


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ("bus", "Bus"),
        ("train", "Train"),
        ("flight", "Flight"),
        ("payment", "Payment"),
        ("booking", "Booking"),
        ("cancel", "Cancellation"),
        ("refund", "Refund"),
        ("account", "Account"),
        ("other", "Other"),
    ]

    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "question"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="support_tickets")
    subject = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="open",)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default="medium",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"

    def __str__(self):
        return f"#{self.id} - {self.subject}"