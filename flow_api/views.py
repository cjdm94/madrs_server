from django.http import JsonResponse
from rest_framework.decorators import api_view
import datetime
from .madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse
from .madrs_self_repo import MadrsSelfSubmissionRepo, MadrsSelfResponseRepo
from .madrs_self_api import CreateMadrsSelfPatientSubmissionSerializer, AddMadrsSelfPatientSubmissionSerializer

mock_madrs_self_mean_scores = {
    'q1': 3,
    'q2': 4,
    'q3': 5,
    'q4': 3,
    'q5': 4,
    'q6': 5,
    'q7': 3,
    'q8': 4,
    'q9': 6,
    'q10': 1
}

@api_view(['POST'])
def create_madrs_self_patient_submission(request):
    serializer = CreateMadrsSelfPatientSubmissionSerializer(
        data={'patient_id': request.data.get('patientId')}
    )
    serializer.is_valid(raise_exception=True)
    patient_id = serializer.data.get('patient_id')

    submission = MadrsSelfSubmission(id=None, patient_id=patient_id, responses=None)
    submissionId = MadrsSelfSubmissionRepo().create(submission)

    return JsonResponse(data={ "submissionId": submissionId }, safe=False)

@api_view(['POST'])
def add_madrs_self_patient_submission_response(request):
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
    submission.add_response(response)
    created = MadrsSelfResponseRepo().create(response, submission)

    return JsonResponse(data={ 'responseId': created.id }, safe=False)

# for a given patient, get mean for each question across all their submissions
@api_view(['GET'])
def patient_historical_madrs_self_mean_scores(request, patient_id):
    # do this with a single sql query
    return JsonResponse(data={
        "count": 1,
        "data": { 
            "patientId": patient_id, 
            "historical_mean_scores": mock_madrs_self_mean_scores 
        }
    })

# get mean for each question across all submissions by all patients
@api_view(['GET'])
def patients_historical_madrs_self_mean_scores(request):
    # do this with a single sql query
    return JsonResponse(data={
        "count": 3,
        "data": [
            { "patientId": 1, "historical_mean_scores": mock_madrs_self_mean_scores },
            { "patientId": 2, "historical_mean_scores": mock_madrs_self_mean_scores },
            { "patientId": 3, "historical_mean_scores": mock_madrs_self_mean_scores },
        ]
    })

# all patients, with each of their submissions, each with a total score and depression severity
# sorted by total score and with the option to filter on a minimum and/or maximum total score
@api_view(['GET'])
def patients_historical_madrs_self_submissions(request):
    # get all patients with submissions 
    # for each diagnostic_questionnaire_submission, map to a madrs_self_submission, computing total score and depression severity 
    # return here
    return JsonResponse(data={
        "count": 1,
        "filters": [ 
            { "minTotalScore": request.query_params.get('minTotalScore') or 0 }, 
            { "maxTotalScore": request.query_params.get('maxTotalScore') or 60 } 
        ],
        "data": [
            { 
                "patientId": 1, 
                "submissions": [ 
                    { 
                        "completedAt": datetime.date.today(),
                        "total_score": 30, 
                        "depression_severity": "SEVERE_DEPRESSION" 
                    } 
                ] 
            },
        ]
    })

# all patients who responded with a certain score on a certain question
@api_view(['GET'])
def filter_patients_by_madrs_self_question_score(request):
    # do this with a single sql query - need to define the madrs_self_question enum in order to filter
    return JsonResponse(data={
        "count": 3,
        "filters": [ { "test": 4 } ],
        "data": [
            { "patientId": 2 },
            { "patientId": 3 },
        ]
    })
