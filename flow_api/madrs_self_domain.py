from django.db import models
from .common import DiagnosticQuestionnaireType
import uuid

class MadrsSelfSymptoms(models.TextChoices):
    MOOD = 'Mood'
    FEELINGS_OF_UNEASE = 'Feelings of Unease'
    SLEEP = 'Sleep'
    APPETITE = 'Appetite'
    ABILITY_TO_CONCENTRATE = 'Ability to Concentrate'
    INITIATIVE = 'Initiative'
    EMOTIONAL_INVOLVEMENT = 'Emotional Involvement'
    PESSIMISM = 'Pessimism'
    ZEST_FOR_LIFE = 'Zest for Life'

class MadrsSelfSubmissionResponse:
    def __init__(self, id, item_index, submission_id, patient_id, symptom, item_string, score):
        self.id = id or uuid.uuid4()
        self.submission_id = submission_id
        self.patient_id = patient_id
        self.symptom = symptom
        self.item_string = item_string
        self.item_index = item_index
        self.score = score

class MadrsSelfSubmission:
    questionnaire_type = DiagnosticQuestionnaireType.MADRS_SELF
    total_items = len(MadrsSelfSymptoms.choices)
    min_item_score = 0
    max_item_score = 6
    score_increments = 1
    min_total_score = 0
    max_total_score = max_item_score * total_items
    
    def __init__(self, id, patient_id):
        self.id = id or uuid.uuid4()
        self.patient_id = patient_id
        self.responses = []
    
    def add_response(self, response):
        if self.responses is 9:
            raise Exception("Madrs-s submission must have no more than 9 responses")
        
        # todo: figure out how to use enum for symptom
        # if symptom not in MadrsSelfSymptoms.choices:
        #     raise Exception("Invalid Madrs-s symptom: %s" % symptom)
        
        if response.symptom in [r.symptom for r in self.responses]:
            raise Exception("Madrs-s submission already contains response for symptom: %s" % response.symptom)
        
        if response.score < self.min_item_score or response.score > self.max_item_score:
            raise Exception("Invalid Madrs-s item score: %d" % response.score)
        
        response = MadrsSelfSubmissionResponse(
            id=response.id, 
            item_index=len(self.responses),
            submission_id=self.id, 
            patient_id=self.patient_id,
            symptom=response.symptom, 
            item_string=response.item_string, 
            score=response.score
        )
        self.responses.append(response)
    
