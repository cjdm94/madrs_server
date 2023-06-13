from django.db import models

class DiagnosticQuestionnaireType(models.TextChoices):
    MADRS = 'MADRS'
    MADRS_SELF = 'MADRS-S'
    PHQ_9 = 'PHQ_9'
    HDI = 'HDI'
    BDI = 'BDI'
