from django.db import models

class SiteSettings(models.Model):

    website_name = models.CharField(max_length=100)
    support_email = models.EmailField()
    support_phone = models.CharField(max_length=20)
    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True
    )

    maintenance_mode = models.BooleanField(
        default=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

# Create your models here.
