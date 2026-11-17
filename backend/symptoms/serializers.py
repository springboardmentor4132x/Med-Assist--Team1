from rest_framework import serializers
from .models import Symptom, SymptomAssessment

# Display available symptoms
class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'symptom_name', 'description']


# Validate selected symptoms
class SymptomSelectionSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        required=True
    )
    def validate_symptoms(self, value):
        # Check empty selection
        if not value:
            raise serializers.ValidationError(
                "Please select at least one symptom."
            )

        # Check duplicates
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Duplicate symptoms are not allowed."
            )

        # Check whether symptoms exist and are active
        valid_symptoms = Symptom.objects.filter(
            id__in=value,
            is_active=True
        )
        if valid_symptoms.count() != len(value):
            raise serializers.ValidationError(
                "One or more selected symptoms are invalid or inactive."
            )
        return value

# Display saved assessments
class SymptomAssessmentSerializer(serializers.ModelSerializer):
    selected_symptoms = SymptomSerializer(many=True, read_only=True)
    class Meta:
        model = SymptomAssessment
        fields = [
            'id',
            'selected_symptoms',
            'assessment_date',
            'validation_status'
        ]