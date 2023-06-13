import unittest
from madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MadrsSelfSymptoms, MadrsSelfSeverityCategories
import json

submission_id = 'submission-1'
patient_id = 'patient-1'

stubbed_responses = {
    MadrsSelfSymptoms.MOOD: MadrsSelfSubmissionResponse(
        id='mood-response', 
        item_index=0, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.MOOD.value,
        item_string='Here you should try to indicate your mood.',
        score=0
    ),
    MadrsSelfSymptoms.FEELINGS_OF_UNEASE: MadrsSelfSubmissionResponse(
        id='unease-response', 
        item_index=1, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.FEELINGS_OF_UNEASE.value,
        item_string='Here you should indicate to what extent you have had feelings of inner tension.',
        score=1
    ),
    MadrsSelfSymptoms.SLEEP: MadrsSelfSubmissionResponse(
        id='sleep-response', 
        item_index=2, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.SLEEP.value,
        item_string='Here you should indicate how well you sleep.',
        score=2
    ),
    MadrsSelfSymptoms.APPETITE: MadrsSelfSubmissionResponse(
        id='appetite-response', 
        item_index=3, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.APPETITE.value,
        item_string='Here you should indicate how your appetite has been.',
        score=3
    ),
    MadrsSelfSymptoms.ABILITY_TO_CONCENTRATE: MadrsSelfSubmissionResponse(
        id='concentration-response', 
        item_index=4, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.ABILITY_TO_CONCENTRATE.value,
        item_string='Here you should try to indicate your ability to collect your thoughts.',
        score=4
    ),
    MadrsSelfSymptoms.INITIATIVE: MadrsSelfSubmissionResponse(
        id='initiative-response', 
        item_index=5, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.INITIATIVE.value,
        item_string='Here you should try to assess your ability to get things done.',
        score=5
    ),
    MadrsSelfSymptoms.EMOTIONAL_INVOLVEMENT: MadrsSelfSubmissionResponse(
        id='emotional-involvement-response', 
        item_index=6, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.EMOTIONAL_INVOLVEMENT.value,
        item_string='Here you should assess your interest in your surroundings.',
        score=6
    ),
    MadrsSelfSymptoms.PESSIMISM: MadrsSelfSubmissionResponse(
        id='pessimism-response', 
        item_index=7, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.PESSIMISM.value,
        item_string='Here you should consider how you view your future.',
        score=0
    ),
    MadrsSelfSymptoms.ZEST_FOR_LIFE: MadrsSelfSubmissionResponse(
        id='zest-for-life-response', 
        item_index=8, 
        submission_id=submission_id, 
        patient_id=patient_id,
        symptom=MadrsSelfSymptoms.ZEST_FOR_LIFE.value,
        item_string='This item concerns your appetite for life.',
        score=1
    ),
}

class TestMadrsSelfSubmission(unittest.TestCase):
    def test_add_response(self):
        submission = MadrsSelfSubmission(
            id=submission_id, 
            patient_id=patient_id,
            responses=None
        )
        
        for response in stubbed_responses.values():
          submission.add_response(response)

        for idx, response in enumerate(submission.responses):
            self.assertEqual(
                vars(submission.responses[idx]), 
                vars(list(stubbed_responses.values())[idx])
            )
        
        self.assertEqual(submission.total_score(), 22)
        self.assertEqual(submission.depression_severity(), MadrsSelfSeverityCategories.MODERATE_DEPRESSION)
    
    def test_add_response_err_max_responses(self):
        submission = MadrsSelfSubmission(
            id=submission_id, 
            patient_id=patient_id,
            responses=None
        )
        
        for response in stubbed_responses.values():
          submission.add_response(response)

        with self.assertRaises(Exception):
           submission.add_response(stubbed_responses.get(MadrsSelfSymptoms.ZEST_FOR_LIFE))

    def test_add_response_err_invalid_symptom(self):
        submission = MadrsSelfSubmission(
            id=submission_id, 
            patient_id=patient_id,
            responses=None
        )
        
        with self.assertRaises(Exception):
            submission.add_response(MadrsSelfSubmissionResponse(
                id='suicidal-ideation-response', 
                item_index=9, 
                submission_id=submission_id, 
                patient_id=patient_id,
                symptom='SUICIDAL_IDEATION',
                item_string='Representing the feeling that life is not worth living.',
                score=0
            ))
    
    def test_add_response_err_duplicate_symptom(self):
        submission = MadrsSelfSubmission(
            id=submission_id, 
            patient_id=patient_id,
            responses=None
        )

        submission.add_response(stubbed_responses.get(MadrsSelfSymptoms.MOOD))      
        with self.assertRaises(Exception):
            submission.add_response(stubbed_responses.get(MadrsSelfSymptoms.MOOD))
    
    def test_add_response_err_score_too_low(self):
        submission = MadrsSelfSubmission(
            id=submission_id, 
            patient_id=patient_id,
            responses=None
        )

        with self.assertRaises(Exception):
            submission.add_response(MadrsSelfSubmissionResponse(
                id='mood-response', 
                item_index=0, 
                submission_id=submission_id, 
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.MOOD.value,
                item_string='Here you should try to indicate your mood.',
                score=-1
            ))
    
    def test_add_response_err_score_too_high(self):
        submission = MadrsSelfSubmission(
            id=submission_id, 
            patient_id=patient_id,
            responses=None
        )

        with self.assertRaises(Exception):
            submission.add_response(MadrsSelfSubmissionResponse(
                id='mood-response', 
                item_index=0, 
                submission_id=submission_id, 
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.MOOD.value,
                item_string='Here you should try to indicate your mood.',
                score=10
            ))

if __name__ == "__main__":
    unittest.main()