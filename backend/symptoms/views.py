from django.db import transaction
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Symptom, SymptomAssessment
from .serializers import (
    SymptomSerializer,
    SymptomSelectionSerializer,
    SymptomAssessmentSerializer
)

# 1. Get all active symptoms and search symptoms
class SymptomListView(generics.ListAPIView):
    serializer_class = SymptomSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = Symptom.objects.filter(is_active=True)
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                symptom_name__icontains=search
            )
        return queryset.order_by('symptom_name')

# 2. Submit selected symptoms
class SymptomSelectionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SymptomSelectionSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        symptom_ids = serializer.validated_data['symptoms']
        # Create assessment and save selected symptoms
        with transaction.atomic():
            assessment = SymptomAssessment.objects.create(
                user=request.user,
                validation_status='valid'
            )
            assessment.selected_symptoms.set(symptom_ids)
        return Response(
            {
                'success': True,
                'message': 'Symptoms submitted successfully.',
                'assessment_id': assessment.id,
                'assessment_date': assessment.assessment_date,
                'validation_status': assessment.validation_status,
                'user_id': request.user.id,
                'symptoms': SymptomSerializer(
                    assessment.selected_symptoms.all(),
                    many=True
                ).data
            },
            status=status.HTTP_201_CREATED
        )

# 3. Retrieve logged-in user's assessments
class MySymptomAssessmentsView(generics.ListAPIView):
    serializer_class = SymptomAssessmentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return SymptomAssessment.objects.filter(
            user=self.request.user
        ).order_by('-assessment_date')