from .madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MadrsSelfSymptoms
from .models import DiagnosticQuestionnaireSubmission, DiagnosticQuestionnaireSubmissionResponse

def madrs_self_submission_response(diagnostic_questionnaire_response):
    return MadrsSelfSubmissionResponse(
        id=diagnostic_questionnaire_response.id,
        item_index=diagnostic_questionnaire_response.item_index,
        submission_id=diagnostic_questionnaire_response.submission.id, 
        patient_id=diagnostic_questionnaire_response.patient_id,
        symptom=diagnostic_questionnaire_response.symptom, 
        item_string=diagnostic_questionnaire_response.item_string, 
        score=diagnostic_questionnaire_response.patient_score
    )

class MadrsSelfSubmissionRepo:
    model = DiagnosticQuestionnaireSubmission
    responseModel = DiagnosticQuestionnaireSubmissionResponse

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
    
    def get_submission_responses(self, submission_id):
        responses = self.responseModel.objects.filter(submission_id=submission_id)
        return [madrs_self_submission_response(r) for r in responses]

    def get(self, submission_id):
        submission = self.model.objects.get(id=submission_id)
        responses = self.get_submission_responses(submission_id)
        return MadrsSelfSubmission(
            id=submission.id, 
            patient_id=submission.patient_id, 
            responses=responses
        )
        
class MadrsSelfResponseRepo:
    model = DiagnosticQuestionnaireSubmissionResponse

    def create(self, response, submission):
        if not MadrsSelfSymptoms.valid(response.symptom):
            raise Exception("Invalid Madrs-s symptom: %s" % response.symptom)
        
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
        return madrs_self_submission_response(created)

