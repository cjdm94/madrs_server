"""
URL configuration for flow_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flow_api import views 

urlpatterns = [
    path('admin/', admin.site.urls),

    # for a given patient, get mean for each question across all their submissions
    path('patient/<int:id>/madrs-s/submissions/mean-scores', views.patient_historical_madrs_s_mean_scores),
    # get mean for each question across all submissions by all patients
    path('patients/madrs-s/submissions/mean-scores', views.patients_historical_madrs_s_submissions),
    # get all patients who responded with a certain score on a certain question (query string)
    path('patients/madrs-s', views.filter_patients_by_madrs_s_question_score),
    # all patients, with each of their submissions, each with a total score and depression severity
    # sorted by total score and with the option to filter on a minimum and/or maximum total score
    # query params (min-total-score, max-total-score)
    path('patients/madrs-s/submissions', views.patients_historical_madrs_s_submissions)
]
