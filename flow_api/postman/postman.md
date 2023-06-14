1. `POST http://localhost:8000/mdrs-self/submission { "patientId": "1" }`

2. `POST http://localhost:8000/mdrs-self/submission/response <submissionData>` 

```
{ "submissionId": "", "symptom": "MOOD", "itemString": "mood string", "score": 5 }

{ "submissionId": "", "symptom": "FEELINGS_OF_UNEASE", "itemString": "unease string", "score": 2 }

{ "submissionId": "", "symptom": "SLEEP", "itemString": "sleep string", "score": 3 }

{ "submissionId": "", "symptom": "APPETITE", "itemString": "appetite string", "score": 1 }

{ "submissionId": "", "symptom": "ABILITY_TO_CONCENTRATE", "itemString": "concentration string", "score": 0 }

{ "submissionId": "", "symptom": "INITIATIVE", "itemString": "initiative string", "score": 3 }

{ "submissionId": "", "symptom": "EMOTIONAL_INVOLVEMENT", "itemString": "emotional-invovlement string", "score": 4 }

{ "submissionId": "", "symptom": "PESSIMISM", "itemString": "pessimism-string", "score": 5 }

{ "submissionId": "", "symptom": "ZEST_FOR_LIFE", "itemString": "life-zest string", "score": 2 }

```
3. `GET http://localhost:8000/patients/madrs-self?symptom=MOOD&score=5`

4. `GET http://localhost:8000/patient/1/madrs-self/submissions/mean-scores`

5. `GET http://localhost:8000/patients/madrs-self/submissions`