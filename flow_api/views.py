from django.http import JsonResponse
from rest_framework.decorators import api_view
from flow_api.madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MADRS_SELF_MIN_TOTAL_SCORE, MADRS_SELF_MAX_TOTAL_SCORE
from flow_api.madrs_self_repo import MadrsSelfSubmissionRepo, MadrsSelfResponseRepo
from flow_api.madrs_self_api import CreateMadrsSelfPatientSubmissionSerializer, AddMadrsSelfPatientSubmissionSerializer, FilterPatientsByMadrsSelfSymptomScoreSerializer, GetPatientHistoricalMadrsSelfMeanSymptomScoresSerializer, GetPatientsHistoricalMadrsSelfSubmissionsSerializer


@api_view(['POST'])
def create_madrs_self_patient_submission(request):
    '''Creates a submission - a container for a patient's responses to an instance of the MARRS-S questionnaire'''
    serializer = CreateMadrsSelfPatientSubmissionSerializer(
        data={'patient_id': request.data.get('patientId')}
    )
    serializer.is_valid(raise_exception=True)
    patient_id = serializer.data.get('patient_id')

    try:
        submission = MadrsSelfSubmission(
            id=None, patient_id=patient_id, responses=None)
        submissionId = MadrsSelfSubmissionRepo().create(submission)
        return JsonResponse(data={"submission_id": submissionId}, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e.args}, status=500)


@api_view(['POST'])
def add_madrs_self_patient_submission_response(request):
    '''Assigns to an existing submission a patient's response to a particular item of the MARRS-S questionnaire'''
    serializer = AddMadrsSelfPatientSubmissionSerializer(
        data={
            'submission_id': request.data.get('submissionId'),
            'symptom': request.data.get('symptom'),
            'item_string': request.data.get('itemString'),
            'score': request.data.get('score')
        }
    )
    serializer.is_valid(raise_exception=True)
    submission_id = serializer.data.get('submission_id')

    try:
        # in the domain/application layer we represent the submission from the database, with its related responses
        submission_repo = MadrsSelfSubmissionRepo()
        submission = submission_repo.get(submission_id)

        response = MadrsSelfSubmissionResponse(
            id=None,
            item_index=len(submission.responses),
            submission_id=submission_id,
            patient_id=submission.patient_id,
            symptom=serializer.data.get('symptom'),
            item_string=serializer.data.get('item_string'),
            score=serializer.data.get('score')
        )
        # and our submission "domain object" enforces the MADRS-S structure and rules
        # to ensure the incoming response is valid in its own right, and with respect to the submission's existing responses
        submission.add_response(response)
        created = MadrsSelfResponseRepo().create(response, submission)

        return JsonResponse(data={'response_id': created.id}, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e.args}, status=500)


@api_view(['GET'])
def patient_historical_madrs_self_mean_scores(request, patient_id):
    '''For a given patient, get mean for each question across all their submissions'''
    serializer = GetPatientHistoricalMadrsSelfMeanSymptomScoresSerializer(
        data={'patient_id': patient_id}
    )
    serializer.is_valid(raise_exception=True)
    patient_id = serializer.data.get('patient_id')

    try:
        response_repo = MadrsSelfResponseRepo()
        mean_score_by_symptom = response_repo.get_patient_historical_mean_all_symptoms(
            patient_id=patient_id)
        return JsonResponse(data={'data': {
            'patient_id': patient_id,
            'historical_mean_scores': mean_score_by_symptom
        }})
    except Exception as e:
        return JsonResponse(data={'error': e.args}, status=500)


@api_view(['GET'])
def patients_historical_madrs_self_mean_scores(request):
    '''Get mean avg for each question across all submissions by all patients'''
    try:
        response_repo = MadrsSelfResponseRepo()
        mean_score_by_symptom = response_repo.get_historical_mean_all_symptoms_all_patients()
        return JsonResponse(data={'data': mean_score_by_symptom})
    except Exception as e:
        return JsonResponse(data={'error': e.args}, status=500)


@api_view(['GET'])
def patients_historical_madrs_self_submissions(request):
    '''
    all patients (with each of their submissions) each with a total score and depression severity 
    sorted by total score and with the option to filter on a minimum and/or maximum total score
    '''
    serializer = GetPatientsHistoricalMadrsSelfSubmissionsSerializer(
        data={
            'min_total_score': request.query_params.get('minTotalScore') or MADRS_SELF_MIN_TOTAL_SCORE,
            'max_total_score': request.query_params.get('maxTotalScore') or MADRS_SELF_MAX_TOTAL_SCORE,
        }
    )
    serializer.is_valid(raise_exception=True)

    try:
        min_total_score = serializer.data.get('min_total_score')
        max_total_score = serializer.data.get('max_total_score')

        submission_repo = MadrsSelfSubmissionRepo()
        submissions_by_patient = submission_repo.get_all_grouped_by_patient()
        patient_submission_summaries = [
            {
                'submission_id': s.id,
                'patient_id': s.patient_id,
                'total_items': s.total_items,
                'items_completed': len(s.responses),
                'total_score': s.total_score(),
                'severity': s.depression_severity().value,
            } for s in submissions_by_patient
        ]

        # AHA! I should be storing the total score in the Submission table. Storage cheaper than computation!! Doh.
        # Then we could do both these in the data layer - more efficient than computing score, filtering and sorting, every time
        filtered_by_total_score = [
            s for s in patient_submission_summaries if min_total_score <= s['total_score'] <= max_total_score]
        sorted_by_total_score = sorted(
            filtered_by_total_score, key=lambda d: d['total_score'])

        return JsonResponse(data={'data': sorted_by_total_score})
    except Exception as e:
        return JsonResponse(data={'error': e.args}, status=500)


@api_view(['GET'])
def filter_patients_by_madrs_self_question_score(request):
    '''All patients who responded with a certain score on a certain question'''
    serializer = FilterPatientsByMadrsSelfSymptomScoreSerializer(
        data={
            'symptom': request.query_params.get('symptom'),
            'score': request.query_params.get('score'),
        }
    )
    serializer.is_valid(raise_exception=True)

    try:
        symptom = serializer.data.get('symptom')
        score = serializer.data.get('score')

        response_repo = MadrsSelfResponseRepo()
        patients = response_repo.filter_patients_with_symptom_score(
            symptom=symptom,
            score=score,
        )
        return JsonResponse(data={
            'count': len(patients),
            'data': patients,
            'filters': [
                {'symptom': symptom},
                {'score': score}
            ],
        })
    except Exception as e:
        return JsonResponse(data={'error': e.args}, status=500)
