from django.db import models

class DiagnosticQuestionnaire(models.Model):
    MADRS_S = 'Madrs-s'
    MADRS = 'Madrs'
    PHQ_9 = 'Phq-9' 
    DIAGNOSTIC_QUESTIONNAIRES = (
        (MADRS_S, 'Madrs-s'),
        (MADRS, 'Madrs'),
        (PHQ_9, 'Phq-9'),
    )

    questionnaire_name = models.CharField(
        max_length=7,
        choices=DIAGNOSTIC_QUESTIONNAIRES,
        default=MADRS,
    )
