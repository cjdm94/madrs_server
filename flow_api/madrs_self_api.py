from rest_framework import serializers
from flow_api.madrs_self_domain import MadrsSelfSymptoms, MADRS_SELF_MIN_TOTAL_SCORE, MADRS_SELF_MAX_TOTAL_SCORE


class CreateMadrsSelfPatientSubmissionSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()


class AddMadrsSelfPatientSubmissionSerializer(serializers.Serializer):
    submission_id = serializers.UUIDField()
    symptom = serializers.ChoiceField(MadrsSelfSymptoms.sequence())
    item_string = serializers.CharField()
    score = serializers.IntegerField()


class FilterPatientsByMadrsSelfSymptomScoreSerializer(serializers.Serializer):
    symptom = serializers.ChoiceField(MadrsSelfSymptoms.sequence())
    score = serializers.IntegerField()


class GetPatientHistoricalMadrsSelfMeanSymptomScoresSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()


class GetPatientsHistoricalMadrsSelfSubmissionsSerializer(serializers.Serializer):
    min_total_score = serializers.IntegerField(
        required=False,
        min_value=MADRS_SELF_MIN_TOTAL_SCORE,
        max_value=MADRS_SELF_MAX_TOTAL_SCORE,
        default=MADRS_SELF_MIN_TOTAL_SCORE
    )
    max_total_score = serializers.IntegerField(
        required=False,
        min_value=MADRS_SELF_MIN_TOTAL_SCORE,
        max_value=MADRS_SELF_MAX_TOTAL_SCORE,
        default=MADRS_SELF_MAX_TOTAL_SCORE
    )
