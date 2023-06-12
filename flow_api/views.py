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

# get mean for each question across all submissions by all patients
@api_view(['GET'])
def patients_historical_madrs_s_mean_scores(request):
    return JsonResponse(data={
        "patientId": 1,
        "mean_scores": mock_madrs_s_mean_scores
    })

# for a given patient, get mean for each question across all their submissions
@api_view(['GET'])
def patient_historical_madrs_s_mean_scores(request, id):
    return JsonResponse(data={
        "count": 3,
        "data": [
            { "patientId": 1, "mean_scores": mock_madrs_s_mean_scores },
            { "patientId": 2, "mean_scores": mock_madrs_s_mean_scores },
            { "patientId": 3, "mean_scores": mock_madrs_s_mean_scores },
        ]
    })

# all patients who responded with a certain score on a certain question
def filter_patients_by_madrs_s_question_score(request):
    return JsonResponse(data={
        "count": 3,
        "data": [
            { "patientId": 2, "mean_scores": mock_madrs_s_mean_scores },
            { "patientId": 3, "mean_scores": mock_madrs_s_mean_scores },
        ]
    })

# all patients, with each of their submissions, each with a total score and depression severity
# sorted by total score and with the option to filter on a minimum and/or maximum total score
def patients_historical_madrs_s_submissions(request):
    return JsonResponse(data={
        "count": 1,
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
