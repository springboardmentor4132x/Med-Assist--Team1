from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('clinic', 'Clinic'),
        ('administrator', 'Administrator'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=10)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'
    )
    def __str__(self):
        return f"{self.user.email} - {self.role}"