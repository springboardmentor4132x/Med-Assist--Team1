from django.conf import settings
from django.db import models

class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class MedicalHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_history_entries",
    )
    condition_name = models.CharField(max_length=150)
    notes = models.TextField(blank=True)
    recorded_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_on", "-created_at"]

    def __str__(self):
        return f"{self.condition_name} ({self.user})"

class SymptomAssessment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="symptom_assessments",
    )
    symptoms = models.ManyToManyField(Symptom, related_name="assessments")
    medical_history_snapshot = models.JSONField(default=list, blank=True)
    correlation_summary = models.JSONField(default=dict, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Assessment {self.pk} - {self.user}"
