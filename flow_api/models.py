from django.db import models

class DiagnosticQuestionnaireSubmission(models.Model):
    MADRS_S = 'Madrs-s'
    MADRS = 'Madrs'
    PHQ_9 = 'Phq-9' 
    DIAGNOSTIC_QUESTIONNAIRE = (
        (MADRS_S, 'Madrs-s'),
        (MADRS, 'Madrs'),
        (PHQ_9, 'Phq-9'),
    )

    questionnaire_name = models.CharField(
        max_length=7,
        choices=DIAGNOSTIC_QUESTIONNAIRE,
        default=MADRS,
    )
