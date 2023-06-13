from django.db.models import Avg, FloatField
from django.db.models.functions import Round
from flow_api.madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MadrsSelfSymptoms
from flow_api.models import DiagnosticQuestionnaireSubmission, DiagnosticQuestionnaireSubmissionResponse


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


def madrs_self_submission(diagnostic_questionnaire_submission, responses):
    return MadrsSelfSubmission(
        id=diagnostic_questionnaire_submission.id,
        patient_id=diagnostic_questionnaire_submission.patient_id,
        responses=responses
    )

# todo: I'd like to have `add_response`` / `add_responses`` methods but I'm not sure how to make it work
# relationally with Django's models ORM, and don't want to spend too much time here


class MadrsSelfSubmissionRepo:
    submission = DiagnosticQuestionnaireSubmission
    submission_response = DiagnosticQuestionnaireSubmissionResponse

    def create(self, submission):
        diagnosticQSubmission = DiagnosticQuestionnaireSubmission(
            id=submission.id,
            patient_id=submission.patient_id
        )

        created = self.submission.objects.create(
            id=diagnosticQSubmission.id,
            patient_id=diagnosticQSubmission.patient_id
        )
        created.save()
        return created.id

    def __get_submission_responses(self, submission_id):
        responses = self.submission_response.objects.filter(
            submission_id=submission_id)
        return [madrs_self_submission_response(r) for r in responses]

    def get(self, submission_id):
        submission = self.submission.objects.get(id=submission_id)
        responses = self.__get_submission_responses(submission_id)
        return madrs_self_submission(submission, responses)

    # querying is inefficient here; should set up the relational model so that I can fetched submissions with their responses
    # todo: is distinct necessary?
    def get_all_grouped_by_patient(self):
        submissions = self.submission.objects.all().distinct().order_by('patient_id', 'id')
        return [madrs_self_submission(s, self.__get_submission_responses(s.id)) for s in submissions]


class MadrsSelfResponseRepo:
    submission_response = DiagnosticQuestionnaireSubmissionResponse

    def create(self, response, submission):
        if not MadrsSelfSymptoms.valid(response.symptom):
            raise Exception("Invalid Madrs-s symptom: %s" % response.symptom)

        diagnosticQSubmission = DiagnosticQuestionnaireSubmission(
            id=submission.id,
            patient_id=submission.patient_id
        )

        created = self.submission_response.objects.create(
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

    def filter_patients_with_symptom_score(self, symptom, score):
        patient_ids = self.submission_response.objects.filter(
            symptom=symptom, patient_score=score).values_list('patient_id', flat=True).distinct()
        print({patient_ids})
        return [{'patient_id': p} for p in patient_ids]

    def get_patient_historical_mean_all_symptoms(self, patient_id):
        responses = self.submission_response.objects.filter(patient_id=patient_id).values('symptom', 'item_index').order_by('item_index').annotate(
            mean_score=Round(Avg('patient_score'), 2, output_field=FloatField()))
        return [
            {'symptom': r['symptom'], 'mean_score': r['mean_score'],
                'item_index': r['item_index']}
            for r in responses
        ]

    # *I think this is average by observation, not average by patient (avg of avg)
    def get_historical_mean_all_symptoms_all_patients(self):
        responses = self.submission_response.objects.values('symptom', 'item_index').order_by('item_index').annotate(
            mean_score=Round(Avg('patient_score'), 2, output_field=FloatField()))
        return [
            {'symptom': r['symptom'], 'mean_score': r['mean_score'],
                'item_index': r['item_index']}
            for r in responses
        ]
