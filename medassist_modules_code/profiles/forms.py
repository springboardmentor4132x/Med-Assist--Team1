from django import forms
from .models import PatientProfile

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ["full_name", "age", "gender", "contact_number"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "age": forms.NumberInput(attrs={"min": 1, "max": 120}),
            "contact_number": forms.TextInput(attrs={"placeholder": "Contact number"}),
        }

    def clean_full_name(self):
        value = self.cleaned_data["full_name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Enter a valid full name.")
        return value

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and not 1 <= age <= 120:
            raise forms.ValidationError("Age must be between 1 and 120.")
        return age

    def clean_contact_number(self):
        value = self.cleaned_data.get("contact_number", "").strip()
        if value and not value.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise forms.ValidationError("Enter a valid contact number.")
        return value
