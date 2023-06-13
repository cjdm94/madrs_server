from django.db import models
from .common import DiagnosticQuestionnaireType
import uuid
from enum import Enum

class MadrsSelfSymptoms(Enum):
    MOOD = 'MOOD'
    FEELINGS_OF_UNEASE = 'FEELINGS_OF_UNEASE'
    SLEEP = 'SLEEP'
    APPETITE = 'APPETITE'
    ABILITY_TO_CONCENTRATE = 'ABILITY_TO_CONCENTRATE'
    INITIATIVE = 'INITIATIVE'
    EMOTIONAL_INVOLVEMENT = 'EMOTIONAL_INVOLVEMENT'
    PESSIMISM = 'PESSIMISM'
    ZEST_FOR_LIFE = 'ZEST_FOR_LIFE'

    # may the Python gods forgive me for this blasphemy (I don't even know but I strongly suspect it's horrible...)
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def sequence(cls):
        return tuple(map(lambda x: (x, x), cls.list()))

    @classmethod
    def valid(cls, symptom):
        return symptom in cls.list()


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
    total_items = len(MadrsSelfSymptoms.list())
    min_item_score = 0
    max_item_score = 6
    score_increments = 1
    min_total_score = 0
    max_total_score = max_item_score * total_items
    
    def __init__(self, id, patient_id, responses):
        self.id = id or uuid.uuid4()
        self.responses = responses or []
        self.patient_id = patient_id
    
    def add_response(self, response):
        if self.responses is self.total_items:
            raise Exception("Madrs-s submission must have no more than %d responses" % self.total_items)
        
        if not MadrsSelfSymptoms.valid(response.symptom):
            raise Exception("Invalid Madrs-s symptom: %s" % response.symptom)
        
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
    
