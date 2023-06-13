from django.db import models
import uuid
from flow_api.madrs_self_domain import MadrsSelfSymptoms


class DiagnosticQuestionnaireSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questionnaire_type = models.TextField()
    # change to email field for demonstration purposes
    patient_id = models.IntegerField()


class DiagnosticQuestionnaireSubmissionResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # change to email field for demonstration purposes
    patient_id = models.IntegerField()
    questionnaire_type = models.TextField()
    submission = models.ForeignKey(
        DiagnosticQuestionnaireSubmission, on_delete=models.CASCADE)
    symptom = models.TextField(choices=MadrsSelfSymptoms.sequence())
    item_string = models.TextField()
    item_index = models.IntegerField()
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    score_increments = models.IntegerField()
    patient_score = models.IntegerField()
