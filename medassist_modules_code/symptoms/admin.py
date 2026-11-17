from django.contrib import admin
from .models import Symptom, MedicalHistory, SymptomAssessment

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("condition_name", "user", "recorded_on")
    search_fields = ("condition_name", "user__username")

@admin.register(SymptomAssessment)
class SymptomAssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "submitted_at")
