from django.test import TestCase
from flow_api.madrs_self_repo import MadrsSelfSubmissionRepo, MadrsSelfResponseRepo
from flow_api.madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MadrsSelfSymptoms


class TestSeeder:
    submission_repo = MadrsSelfSubmissionRepo()
    response_repo = MadrsSelfResponseRepo()

    def create_complete_submission(self, patient_id, submission_id, scores):
        submission = MadrsSelfSubmission(1, 'callum@gaia.family', None)
        self.submission_repo.create(submission)

        complete_response_set = {
            MadrsSelfSymptoms.MOOD: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'mood-response',
                item_index=0,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.MOOD.value,
                item_string='Here you should try to indicate your mood.',
                score=scores[0]
            ),
            MadrsSelfSymptoms.FEELINGS_OF_UNEASE: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'unease-response',
                item_index=1,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.FEELINGS_OF_UNEASE.value,
                item_string='Here you should indicate to what extent you have had feelings of inner tension.',
                score=scores[1]
            ),
            MadrsSelfSymptoms.SLEEP: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'sleep-response',
                item_index=2,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.SLEEP.value,
                item_string='Here you should indicate how well you sleep.',
                score=scores[2]
            ),
            MadrsSelfSymptoms.APPETITE: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'appetite-response',
                item_index=3,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.APPETITE.value,
                item_string='Here you should indicate how your appetite has been.',
                score=scores[3]
            ),
            MadrsSelfSymptoms.ABILITY_TO_CONCENTRATE: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'concentration-response',
                item_index=4,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.ABILITY_TO_CONCENTRATE.value,
                item_string='Here you should try to indicate your ability to collect your thoughts.',
                score=scores[4]
            ),
            MadrsSelfSymptoms.INITIATIVE: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'initiative-response',
                item_index=5,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.INITIATIVE.value,
                item_string='Here you should try to assess your ability to get things done.',
                score=scores[5]
            ),
            MadrsSelfSymptoms.EMOTIONAL_INVOLVEMENT: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'emotional-involvement-response',
                item_index=6,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.EMOTIONAL_INVOLVEMENT.value,
                item_string='Here you should assess your interest in your surroundings.',
                score=scores[6]
            ),
            MadrsSelfSymptoms.PESSIMISM: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'pessimism-response',
                item_index=7,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.PESSIMISM.value,
                item_string='Here you should consider how you view your future.',
                score=scores[7]
            ),
            MadrsSelfSymptoms.ZEST_FOR_LIFE: MadrsSelfSubmissionResponse(
                id=patient_id + submission_id + 'zest-for-life-response',
                item_index=8,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.ZEST_FOR_LIFE.value,
                item_string='This item concerns your appetite for life.',
                score=scores[8]
            ),
        }

        for response in complete_response_set.values():
            submission.add_response(response)


class TestMadrsSelfRepo(TestCase):
    def setUp(self):
        seeder = TestSeeder()
        seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=1,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=2,
            scores=[1, 4, 2, 1, 0, 0, 1, 2, 0]
        )
        seeder.create_complete_submission(
            patient_id='albert@flowneuroscience.com',
            submission_id=3,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        seeder.create_complete_submission(
            patient_id='albert@flowneuroscience.com',
            submission_id=4,
            scores=[1, 4, 2, 1, 0, 0, 1, 2, 0]
        )
        seeder.create_complete_submission(
            patient_id='erik@flowneuroscience.com',
            submission_id=3,
            scores=[5, 5, 2, 6, 1, 0, 2, 4, 2]
        )
        seeder.create_complete_submission(
            patient_id='erik@flowneuroscience.com',
            submission_id=4,
            scores=[0, 0, 3, 4, 4, 1, 5, 1, 0]
        )

    def test_create_submission(self):
        submission_repo = MadrsSelfSubmissionRepo()
        response_repo = MadrsSelfResponseRepo()

        submissions = submission_repo.get_all_grouped_by_patient()
        print(submissions)
