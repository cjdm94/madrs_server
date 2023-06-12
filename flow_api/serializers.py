from rest_framework import serializers
from .models import DiagnosticQuestionnaireSubmission

class DiagnosticQuestionnaireSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticQuestionnaireSubmission
        fields = ['questionnaire_name']
