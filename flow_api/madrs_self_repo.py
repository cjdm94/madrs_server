from .madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse
from .models import DiagnosticQuestionnaireSubmission, DiagnosticQuestionnaireSubmissionResponse

class MadrsSelfSubmissionRepo:
    model = DiagnosticQuestionnaireSubmission

    def create(self, submission):
        diagnosticQSubmission = DiagnosticQuestionnaireSubmission(
            id=submission.id, 
            patient_id=submission.patient_id
        )

        created = self.model.objects.create(
            id=diagnosticQSubmission.id, 
            patient_id=diagnosticQSubmission.patient_id
        )
        created.save()
        return created.id

    def get(self, submission_id):
        submission = self.model.objects.get(id=submission_id)
        return MadrsSelfSubmission(id=submission.id, patient_id=submission.patient_id)

class MadrsSelfResponseRepo:
    model = DiagnosticQuestionnaireSubmissionResponse

    def create(self, response, submission):
        diagnosticQSubmission = DiagnosticQuestionnaireSubmission(
            id=submission.id, 
            patient_id=submission.patient_id
        )

        created = self.model.objects.create(
            id=response.id,
            patient_id=submission.patient_id,
            questionnaire_type=submission.questionnaire_type,
            submission=diagnosticQSubmission,
            symptom=response.symptom,
            item_string=response.item_string,
            item_index=response.item_index,
            min_score=submission.min_item_score,
            max_score=submission.max_item_score,
            score_increments=submission.score_increments,
            patient_score=response.score
        )
        created.save()
        return MadrsSelfSubmissionResponse(
            id=created.id,
            item_index=created.item_index,
            submission_id=created.submission.id, 
            patient_id=created.patient_id,
            symptom=created.symptom, 
            item_string=created.item_string, 
            score=created.patient_score
        )
