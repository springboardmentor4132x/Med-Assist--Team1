from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import MedicalHistoryForm
from .models import Symptom, MedicalHistory, SymptomAssessment
from .correlation import analyse_symptoms

@login_required
def symptom_selection(request):
    symptoms = Symptom.objects.filter(is_active=True)
    if request.method == "POST":
        selected_ids = request.POST.getlist("symptoms")
        if not selected_ids:
            messages.error(request, "Please select at least one symptom.")
            return render(request, "symptoms/symptom_selection.html", {"symptoms": symptoms})

        if len(selected_ids) != len(set(selected_ids)):
            messages.error(request, "Duplicate symptoms were submitted. Please review your selection.")
            return render(request, "symptoms/symptom_selection.html", {"symptoms": symptoms})

        selected = list(Symptom.objects.filter(id__in=selected_ids, is_active=True))
        if len(selected) != len(selected_ids):
            messages.error(request, "One or more selected symptoms are invalid.")
            return render(request, "symptoms/symptom_selection.html", {"symptoms": symptoms})

        names = [s.name for s in selected]
        try:
            correlation = analyse_symptoms(names)
        except (ValueError, KeyError) as exc:
            messages.error(request, str(exc))
            return render(request, "symptoms/symptom_selection.html", {"symptoms": symptoms})

        history = list(
            MedicalHistory.objects.filter(user=request.user).values(
                "condition_name", "notes", "recorded_on"
            )
        )
        assessment = SymptomAssessment.objects.create(
            user=request.user,
            medical_history_snapshot=[
                {
                    "condition_name": item["condition_name"],
                    "notes": item["notes"],
                    "recorded_on": item["recorded_on"].isoformat() if item["recorded_on"] else None,
                } for item in history
            ],
            correlation_summary=correlation,
        )
        assessment.symptoms.set(selected)
        messages.success(request, "Your symptom assessment was saved.")
        return redirect("assessment_detail", assessment_id=assessment.id)

    return render(request, "symptoms/symptom_selection.html", {"symptoms": symptoms})

@login_required
def medical_history_list(request):
    entries = MedicalHistory.objects.filter(user=request.user)
    return render(request, "symptoms/medical_history_list.html", {"entries": entries})

@login_required
def medical_history_add(request):
    if request.method == "POST":
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Medical history entry saved.")
            return redirect("medical_history_list")
    else:
        form = MedicalHistoryForm()
    return render(request, "symptoms/medical_history_form.html", {"form": form})

@login_required
def assessment_history(request):
    assessments = SymptomAssessment.objects.filter(user=request.user)
    return render(request, "symptoms/assessment_history.html", {"assessments": assessments})

@login_required
def assessment_detail(request, assessment_id):
    assessment = get_object_or_404(SymptomAssessment, id=assessment_id, user=request.user)
    return render(request, "symptoms/assessment_detail.html", {"assessment": assessment})
