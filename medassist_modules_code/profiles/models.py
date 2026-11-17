from django.conf import settings
from django.db import models

class PatientProfile(models.Model):
    GENDER_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    full_name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or str(self.user)
