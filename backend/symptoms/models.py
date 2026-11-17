from django.db import models
from django.contrib.auth.models import User

class Symptom(models.Model):
    symptom_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.symptom_name

class SymptomAssessment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='symptom_assessments'
    )
    selected_symptoms = models.ManyToManyField(Symptom)
    assessment_date = models.DateTimeField(auto_now_add=True)
    validation_status = models.CharField(
        max_length=20,
        default='valid'
    )
    def __str__(self):
        return f"Assessment {self.id} - {self.user.username}"