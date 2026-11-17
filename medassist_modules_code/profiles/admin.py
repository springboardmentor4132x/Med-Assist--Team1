from django.contrib import admin
from .models import PatientProfile

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "age", "gender", "updated_at")
    search_fields = ("full_name", "user__username", "user__email")
