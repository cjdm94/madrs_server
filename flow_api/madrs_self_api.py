from rest_framework import serializers

class CreateMadrsSelfPatientSubmissionSerializer(serializers.Serializer):
   patient_id = serializers.IntegerField()

# todo: validate against symptom enum
class AddMadrsSelfPatientSubmissionSerializer(serializers.Serializer):
   submission_id = serializers.UUIDField()
   symptom = serializers.CharField()
   item_string = serializers.CharField()
   score = serializers.IntegerField()