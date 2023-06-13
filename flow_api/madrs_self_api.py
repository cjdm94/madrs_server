from rest_framework import serializers
from .madrs_self_domain import MadrsSelfSymptoms

class CreateMadrsSelfPatientSubmissionSerializer(serializers.Serializer):
   patient_id = serializers.IntegerField()

class AddMadrsSelfPatientSubmissionSerializer(serializers.Serializer):
   submission_id = serializers.UUIDField()
   symptom = serializers.ChoiceField(MadrsSelfSymptoms.sequence())
   item_string = serializers.CharField()
   score = serializers.IntegerField()