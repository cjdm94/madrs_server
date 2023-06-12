from django.http import JsonResponse
from .models import DiagnosticQuestionnaireSubmission
from rest_framework.decorators import api_view
import datetime

mock_madrs_s_mean_scores = {
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
def create_madrs_s_patient_submission(request, id):
    return JsonResponse(data={ "submissionId": 1 })

@api_view(['PUT'])
def add_madrs_s_patient_submission_response(request, id):
    return JsonResponse(data={ "submissionId": 1, "ok": True })

# for a given patient, get mean for each question across all their submissions
@api_view(['GET'])
def patient_historical_madrs_s_mean_scores(request, id):
    # do this with a single sql query
    return JsonResponse(data={
        "count": 1,
        "data": { 
            "patientId": id, 
            "historical_mean_scores": mock_madrs_s_mean_scores 
        }
    })

# get mean for each question across all submissions by all patients
@api_view(['GET'])
def patients_historical_madrs_s_mean_scores(request):
    # do this with a single sql query
    return JsonResponse(data={
        "count": 3,
        "data": [
            { "patientId": 1, "historical_mean_scores": mock_madrs_s_mean_scores },
            { "patientId": 2, "historical_mean_scores": mock_madrs_s_mean_scores },
            { "patientId": 3, "historical_mean_scores": mock_madrs_s_mean_scores },
        ]
    })

# all patients, with each of their submissions, each with a total score and depression severity
# sorted by total score and with the option to filter on a minimum and/or maximum total score
@api_view(['GET'])
def patients_historical_madrs_s_submissions(request):
    # get all patients with submissions 
    # for each diagnostic_questionnaire_submission, map to a madrs_s_submission, computing total score and depression severity 
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
def filter_patients_by_madrs_s_question_score(request):
    # do this with a single sql query - need to define the madrs_s_question enum in order to filter
    return JsonResponse(data={
        "count": 3,
        "filters": [ { "test": 4 } ],
        "data": [
            { "patientId": 2 },
            { "patientId": 3 },
        ]
    })
