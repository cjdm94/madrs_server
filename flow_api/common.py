from django.db import models

class DiagnosticQuestionnaireType(models.TextChoices):
    MADRS = 'Madrs'
    MADRS_SELF = 'Madrs-s'
    PHQ_9 = 'Phq-9'