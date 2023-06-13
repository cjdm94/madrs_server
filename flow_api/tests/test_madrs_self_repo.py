from django.test import TestCase
from flow_api.madrs_self_repo import MadrsSelfSubmissionRepo, MadrsSelfResponseRepo
from flow_api.madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MadrsSelfSymptoms
from flow_api.common import DiagnosticQuestionnaireType


class TestSeeder:
    submission_repo = MadrsSelfSubmissionRepo()
    response_repo = MadrsSelfResponseRepo()

    def create_complete_submission(self, patient_id, submission_id, scores):
        submission = MadrsSelfSubmission(
            id=submission_id,
            patient_id=patient_id,
            responses=None
        )
        self.submission_repo.create(submission)

        complete_response_set = {
            MadrsSelfSymptoms.MOOD: MadrsSelfSubmissionResponse(
                id=None,
                item_index=0,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.MOOD.value,
                item_string='Here you should try to indicate your mood.',
                score=scores[0]
            ),
            MadrsSelfSymptoms.FEELINGS_OF_UNEASE: MadrsSelfSubmissionResponse(
                id=None,
                item_index=1,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.FEELINGS_OF_UNEASE.value,
                item_string='Here you should indicate to what extent you have had feelings of inner tension.',
                score=scores[1]
            ),
            MadrsSelfSymptoms.SLEEP: MadrsSelfSubmissionResponse(
                id=None,
                item_index=2,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.SLEEP.value,
                item_string='Here you should indicate how well you sleep.',
                score=scores[2]
            ),
            MadrsSelfSymptoms.APPETITE: MadrsSelfSubmissionResponse(
                id=None,
                item_index=3,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.APPETITE.value,
                item_string='Here you should indicate how your appetite has been.',
                score=scores[3]
            ),
            MadrsSelfSymptoms.ABILITY_TO_CONCENTRATE: MadrsSelfSubmissionResponse(
                id=None,
                item_index=4,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.ABILITY_TO_CONCENTRATE.value,
                item_string='Here you should try to indicate your ability to collect your thoughts.',
                score=scores[4]
            ),
            MadrsSelfSymptoms.INITIATIVE: MadrsSelfSubmissionResponse(
                id=None,
                item_index=5,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.INITIATIVE.value,
                item_string='Here you should try to assess your ability to get things done.',
                score=scores[5]
            ),
            MadrsSelfSymptoms.EMOTIONAL_INVOLVEMENT: MadrsSelfSubmissionResponse(
                id=None,
                item_index=6,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.EMOTIONAL_INVOLVEMENT.value,
                item_string='Here you should assess your interest in your surroundings.',
                score=scores[6]
            ),
            MadrsSelfSymptoms.PESSIMISM: MadrsSelfSubmissionResponse(
                id=None,
                item_index=7,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.PESSIMISM.value,
                item_string='Here you should consider how you view your future.',
                score=scores[7]
            ),
            MadrsSelfSymptoms.ZEST_FOR_LIFE: MadrsSelfSubmissionResponse(
                id=None,
                item_index=8,
                submission_id=submission_id,
                patient_id=patient_id,
                symptom=MadrsSelfSymptoms.ZEST_FOR_LIFE.value,
                item_string='This item concerns your appetite for life.',
                score=scores[8]
            ),
        }

        for response in complete_response_set.values():
            self.response_repo.create(response, submission)

        return submission.id


class TestMadrsSelfRepo(TestCase):
    def test_create_submission(self):
        seeder = TestSeeder()
        submission_id = seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )

        submission_repo = MadrsSelfSubmissionRepo()
        fetched_submission = submission_repo.get(submission_id)

        # check basic submission data
        self.assertEqual(fetched_submission.id, submission_id)
        self.assertEqual(fetched_submission.patient_id, 'callum@gaia.family')
        self.assertEqual(fetched_submission.questionnaire_type,
                         DiagnosticQuestionnaireType.MADRS_SELF)
        self.assertEqual(len(fetched_submission.responses), 9)

        # check submission-responses data
        self.assertEqual(
            [r.symptom for r in fetched_submission.responses],
            MadrsSelfSymptoms.list()
        )
        self.assertEqual(
            [r.score for r in fetched_submission.responses],
            [3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        self.assertEqual(
            list(set([r.patient_id for r in fetched_submission.responses])),
            ['callum@gaia.family']
        )
        self.assertEqual(
            list(set([r.submission_id for r in fetched_submission.responses])),
            [submission_id]
        )
