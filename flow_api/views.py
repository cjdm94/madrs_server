from django.http import JsonResponse
from .models import DiagnosticQuestionnaireSubmission
from rest_framework.decorators import api_view

# get mean for each question across all submissions by all users
@api_view(['GET'])
def madrs_s_mean_scores_for_submissions(request):
    return JsonResponse(data={ "request_received": True })