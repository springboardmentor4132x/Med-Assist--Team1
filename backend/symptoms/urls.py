from django.urls import path
from .views import(
    SymptomListView,
    SymptomSelectionView,
    MySymptomAssessmentsView
)
urlpatterns=[
    # Get available symptoms
    path(
        '',
        SymptomListView.as_view(),
        name='symptom-list'
    ),
    # Submit selected symptoms
    path(
        'select/',
        SymptomSelectionView.as_view(),
        name='symptom-select'
    ),
    # Get logged-in user's assessments
    path(
        'my-assessments/',
        MySymptomAssessmentsView.as_view(),
        name='my-assessments'
    ),
]