from django import forms
from .models import MedicalHistory

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ["condition_name", "notes", "recorded_on"]
        widgets = {
            "recorded_on": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_condition_name(self):
        value = self.cleaned_data["condition_name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Enter a valid condition name.")
        return value
