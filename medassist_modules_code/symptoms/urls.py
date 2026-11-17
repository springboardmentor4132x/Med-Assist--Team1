from django.urls import path
from . import views

urlpatterns = [
    path("", views.symptom_selection, name="symptom_selection"),
    path("medical-history/", views.medical_history_list, name="medical_history_list"),
    path("medical-history/add/", views.medical_history_add, name="medical_history_add"),
    path("assessments/", views.assessment_history, name="assessment_history"),
    path("assessments/<int:assessment_id>/", views.assessment_detail, name="assessment_detail"),
]
