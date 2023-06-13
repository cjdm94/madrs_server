from django.test import TestCase
from flow_api.madrs_self_repo import MadrsSelfSubmissionRepo, MadrsSelfResponseRepo
from flow_api.madrs_self_domain import MadrsSelfSubmission, MadrsSelfSubmissionResponse, MadrsSelfSymptoms
from flow_api.common import DiagnosticQuestionnaireType


class TestSeeder:
    submission_repo = MadrsSelfSubmissionRepo()
    response_repo = MadrsSelfResponseRepo()

    def seed_default_data(self):
        self.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        self.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[1, 3, 3, 5, 0, 3, 5, 2, 2]
        )
        self.create_complete_submission(
            patient_id='albert@flowneuroscience.com',
            submission_id=None,
            scores=[6, 5, 1, 2, 0, 5, 4, 3, 1]
        )
        self.create_complete_submission(
            patient_id='erik@flowneuroscience.com',
            submission_id=None,
            scores=[2, 0, 0, 1, 0, 1, 4, 2, 0]
        )

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


class TestMadrsSelfSubmissionRepo(TestCase):
    submission_repo = MadrsSelfSubmissionRepo()
    seeder = TestSeeder()

    def test_create_submission(self):
        submission_id = self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )

        fetched_submission = self.submission_repo.get(submission_id)

        # check basic submission data
        self.assertEqual(fetched_submission.id, submission_id)
        self.assertEqual(fetched_submission.patient_id, 'callum@gaia.family')
        self.assertEqual(fetched_submission.questionnaire_type,
                         DiagnosticQuestionnaireType.MADRS_SELF)

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

    def test_get_all_grouped_by_patient(self):
        self.seeder.seed_default_data()
        submissions = self.submission_repo.get_all_grouped_by_patient()
        self.assertEqual(
            [r.patient_id for r in submissions],
            ['albert@flowneuroscience.com', 'callum@gaia.family',
                'callum@gaia.family', 'erik@flowneuroscience.com']
        )


class TestMadrsSelfResponseRepo(TestCase):
    response_repo = MadrsSelfResponseRepo()
    seeder = TestSeeder()

    # todo: a nicer way to run this test on many score combinations
    def test_filter_patients_with_symptom_score(self):
        self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        self.seeder.create_complete_submission(
            patient_id='albert@flowneuroscience.com',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        self.seeder.create_complete_submission(
            patient_id='erik@flowneuroscience.com',
            submission_id=None,
            scores=[0, 2, 3, 4, 1, 0, 2, 3, 5]
        )

        patients = self.response_repo.filter_patients_with_symptom_score(
            MadrsSelfSymptoms.MOOD.value, 3)
        self.assertEqual(patients, [
            {'patient_id': 'callum@gaia.family'},
            {'patient_id': 'albert@flowneuroscience.com'},
        ])

    def test_get_patient_historical_mean_all_symptoms(self):
        self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[5, 3, 4, 3, 2, 5, 4, 4, 3]
        )
        self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[4, 3, 3, 3, 2, 3, 2, 3, 2]
        )
        self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[2, 2, 2, 2, 1, 2, 2, 3, 1]
        )
        # (filtered out in the query)
        self.seeder.create_complete_submission(
            patient_id='albert@flowneuroscience.com',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )

        mean_scores = self.response_repo.get_patient_historical_mean_all_symptoms(
            'callum@gaia.family')

        self.assertEqual(
            [s['item_index'] for s in mean_scores],
            [0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        self.assertEqual(
            [s['symptom'] for s in mean_scores],
            MadrsSelfSymptoms.list()
        )
        self.assertEqual(
            [s['mean_score'] for s in mean_scores],
            [3.67, 2.67, 3.0, 2.67, 1.67, 3.33, 2.67, 3.33, 2.0]
        )

    def test_get_historical_mean_all_symptoms_all_patients(self):
        self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[3, 2, 3, 4, 1, 0, 2, 3, 5]
        )
        self.seeder.create_complete_submission(
            patient_id='callum@gaia.family',
            submission_id=None,
            scores=[1, 3, 3, 5, 0, 3, 5, 2, 2]
        )
        self.seeder.create_complete_submission(
            patient_id='albert@flowneuroscience.com',
            submission_id=None,
            scores=[6, 5, 1, 2, 0, 5, 4, 3, 1]
        )
        self.seeder.create_complete_submission(
            patient_id='erik@flowneuroscience.com',
            submission_id=None,
            scores=[2, 0, 0, 1, 0, 1, 4, 2, 0]
        )

        mean_scores = self.response_repo.get_historical_mean_all_symptoms_all_patients()
        self.assertEqual(
            [s['item_index'] for s in mean_scores],
            [0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        self.assertEqual(
            [s['symptom'] for s in mean_scores],
            MadrsSelfSymptoms.list()
        )
        self.assertEqual(
            [s['mean_score'] for s in mean_scores],
            [3.0, 2.5, 1.75, 3.0, 0.25, 2.25, 3.75, 2.5, 2.0]
        )
