# Solution

Ok. It's 18:23 on Sunday night. It's been a very hot, humid, summery British day. Beautiful. But also, sweaty. Owing to the temperamental British climate (the other day it was max 14C?), I therefore cannot be held responsible for any of the code written in the coming hours.

I have my water, I have my coffee, I have my beer for later, should I find myself lost in the Django abyss. And I have the Interstellar soundtrack for cosmological epicness to keep the motivation high. Let's go.

## Plan of Action

Once I read the task I couldn't help but start to think about the data model.

I'm leaning towards a generic diagnostic-questionnaire model in the persistence layer which does not encode the rules of any particular instantiation. E.g. a more generic/agnostic `DiagnosticQuestionnaire` model - describing the core characteristics of the diagnostic-questionnaire construct - rather than the more concrete `MADRSQuestionaire` model. Then we can have a single table for all the diagnostic questionnaires we support.

The rules of any particular questionnaire model - e.g. the MADRS-s - can then be encoded in the business logic encapsulated in a MADRS-s class (or equivalent), atop the persistence layer. The rules of each particular questionnaire can be modified or extended easily over time, if needed, but we can still rely on our single `DiagnosticQuestionnaire` persistence model.

There is an argument to be made that we are working here with fixed, stable systems that are not liable to change, and hence we could have a table per instantiation - e.g. `MADRS_S_QUESTIONNAIRE`, `MADRS_QUESTIONNAIRE`, `PHQ-9-QUESTIONNAIRE`. However "we are working here with fixed, stable systems that are not liable to change" may be an example of A classic engineering mistake. So my preliminary conclusion is: in the persistence model, defend against unexpected changes and complexity, even though we're modelling a relatively fixed system. Then encode the specific rules of each questionnaire type in the domain layer, and extend this easily over time, if these changes and new complexities do manifest. This gives us extendability, separation of business logic from the persistence layer so our rules can be unit tested well, and ease of querying, with fewer models to manage and maintain.

Having more domain knowledge here would help. For now I'll leave it here, as I've found in the past that starting with the data model can be a fool's errand. I'll build the API endpoint handlers first, with stubbed data, as this might shed some light on how we can model the data most sensibly. 

Time to meet Django!

### A Working API

We have a working Django API. Now for the fun bit! 

Some thoughts I had whilst setting up:

(1) The task spec seems to assume we would only have a single diagnostic questionnaire submission per user. Of course typically patients would take the questionnaire periodically, and then clinicians can monitor the fluctuation of scores over time. I think I'll build it to support historical submissions by users - let's see.

(2) We care about individual questions on specific diagnostic questionnaires, so we need to be able to reliably uniquely identify specific questions, not just particular diagnostic questionnaires. The question is, which parameter should we use as a uid? It seems we have a question string, a question order (the index at which the question appears in the questionnaire), and a symptom that the question is designed to "screen". The latter of the three seems to be the most reliable option: the first two are possibly more susceptible to variability. The particular string might vary between clinicians/clinics, and perhaps the order too (though I suspect this is less likely). The symptom however is at the very core of the diagnostic questionnaire construct itself. Let's see.

### The Fun Part

Alright. We have two principles here: 

(1) We're going to use a more generic, questionnaire-agnostic persistence model - `DiagnosticQuestionnaireSubmission` and `DiagnosticQuestionnaireResponse`
(2) At the API layer we want to keep the interface precise and strict - so we will have specific endpoints for the madrs-s questionnaire, which madrs-s-specific "schemas"

We'll therefore need to create a mapping between our concrete madrs-s model in the API layer and our agnostic persistence model.

So we want:

- A `MadrsSSubmission`, a kind of domain object that we can serialise from the API request
- A `DiagnosticQuestionnaireSubmission` model in the persistence layer
- A `MadrsRepo` which will encapsulate the mapping between the first and the second, which we will unit test

### A note on the submission-response relationship

Really we first have a "submission" (a collection of questions specified by the particular diagnostic model, and corresponding self- or clinician-administered answers). Second, we have an individual "response" per question.

Since the nature of these kinds of diagnostic tools require all questions to be answered collectively in a single submission or session (I don't submit 5 answers now and 5 answers later), we should perhaps force the client to respect this in the way it sends the submission/response data.

I think it would be nicer for the client to send in a single API call the complete submission payload containing the answers to all the questions. This makes it easier for the server to validate the integrity of the data (this is a madrs-s submission, so it should contain 10 questions addressing X,Y,Z symptoms). It also means the submission data exists, in the persistence layer, in a binary state: either we have the records for a complete submission, or we have no records at all. There is no possibility of partially complete submissions.

There is a downside to this approach: if an end user completes a partial submission and then there is some network or other error resulting in a loss of client-side state, they would need to restart the submission. This is especially a danger for direct consumers, because we want to treat them with extreme care during a *self-administered* mental-health questionnaire. For clinicians who are submitting results on behalf of patients, this is less of a concern, also we still run the risk of annoying our partners. 

For now though let's follow the requirements of the task and, each time we write a response to an existing submission, we can just check the existing responses to validate the integrity of the incoming response. We will encapsulate this business logic in the `MadrsSSubmission` domain object mentioned above.