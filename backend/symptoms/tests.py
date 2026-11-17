from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Symptom, SymptomAssessment


class SymptomAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Test@12345"
        )

        self.symptom1 = Symptom.objects.create(
            symptom_name="Fever",
            description="High body temperature",
            is_active=True
        )

        self.symptom2 = Symptom.objects.create(
            symptom_name="Headache",
            description="Pain in head",
            is_active=True
        )

        self.inactive_symptom = Symptom.objects.create(
            symptom_name="Inactive Symptom",
            is_active=False
        )

        self.client.force_authenticate(user=self.user)

    def test_get_symptoms(self):
        response = self.client.get("/api/symptoms/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_submit_valid_symptoms(self):
        response = self.client.post(
            "/api/symptoms/select/",
            {"symptoms": [self.symptom1.id, self.symptom2.id]},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SymptomAssessment.objects.count(), 1)

    def test_empty_symptoms(self):
        response = self.client.post(
            "/api/symptoms/select/",
            {"symptoms": []},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_symptoms(self):
        response = self.client.post(
            "/api/symptoms/select/",
            {"symptoms": [self.symptom1.id, self.symptom1.id]},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_symptom_id(self):
        response = self.client.post(
            "/api/symptoms/select/",
            {"symptoms": [99999]},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_symptom(self):
        response = self.client.post(
            "/api/symptoms/select/",
            {"symptoms": [self.inactive_symptom.id]},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assessment_belongs_to_logged_in_user(self):
        response = self.client.post(
            "/api/symptoms/select/",
            {"symptoms": [self.symptom1.id]},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        assessment = SymptomAssessment.objects.latest("id")
        self.assertEqual(assessment.user, self.user)