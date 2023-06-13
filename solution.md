# Solution

Ok. It's 18:23 on Sunday night. It's been a very hot, humid, summery British day. Beautiful. But also, sweaty. Owing to the temperamental British climate (the other day it was max 14C?), I therefore cannot be held responsible for any of the code written in the coming hours.

I have my water, I have my coffee, I have my beer for later, should I find myself lost in the Django abyss. And I have the Interstellar soundtrack for cosmological epicness to keep the motivation high. Let's go.

## Plan of Action

Once I read the task I couldn't help but start to think about the data model.

I'm leaning towards a generic diagnostic-questionnaire model in the persistence layer which does not encode the rules of any particular instantiation. E.g. a more generic/agnostic `DiagnosticQuestionnaire` model - describing the core characteristics of the diagnostic-questionnaire construct - rather than the more concrete `MADRSQuestionaire` model. Then we can have a single table for all the diagnostic questionnaires we support.

The rules of any particular questionnaire model - e.g. the MADRS-s - can then be encoded in the business logic encapsulated in a MADRS-s class (or equivalent), atop the persistence layer. The rules of each particular questionnaire can be modified or extended easily over time, if needed, but we can still rely on our single `DiagnosticQuestionnaire` persistence model.

There is an argument to be made that we are working here with fixed, stable systems that are not liable to change, and hence we could have a table per instantiation - e.g. `MADRS_S_QUESTIONNAIRE`, `MADRS_QUESTIONNAIRE`, `PHQ-9-QUESTIONNAIRE`. However "we are working here with fixed, stable systems that are not liable to change" may be an example of a classic engineering mistake. So my preliminary conclusion is: in the persistence model, defend against unexpected changes and complexity, even though we're modelling a relatively fixed system. Then encode the specific rules of each questionnaire type in the domain layer, and extend this easily over time, if these changes and new complexities do manifest. This gives us extendability, separation of business logic from the persistence layer so our rules can be unit tested well, and ease of querying, with fewer models to manage and maintain.

Having more domain knowledge here would help. For now I'll leave it here, as I've found in the past that starting with the data model can be a fool's errand. I'll build the API endpoint handlers first, with stubbed data, as this might shed some light on how we can model the data most sensibly. 

Time to meet Django!

## A Working API

We have a working Django API. Now for the fun bit! 

Some thoughts I had whilst setting up:

(1) The task spec seems to assume we would only have a single diagnostic questionnaire submission per user. Of course typically patients would take the questionnaire periodically, and then clinicians can monitor the fluctuation of scores over time. I think I'll build it to support historical submissions by users - let's see.

(2) We care about individual questions on specific diagnostic questionnaires, so we need to be able to reliably uniquely identify specific questions, not just particular diagnostic questionnaires. The question is, which parameter should we use as a uid? It seems we have a question string, a question order (the index at which the question appears in the questionnaire), and a symptom that the question is designed to "screen". The latter of the three seems to be the most reliable option: the first two are possibly more susceptible to variability. The particular string might vary between clinicians/clinics, and perhaps the order too (though I suspect this is less likely). The symptom however is at the very core of the diagnostic questionnaire construct itself. Let's see.

## The Fun Part

Alright. We have two principles here: 

(1) We're going to use a more generic, questionnaire-agnostic persistence model - `DiagnosticQuestionnaireSubmission` and `DiagnosticQuestionnaireResponse`
(2) At the API layer we want to keep the interface precise and strict - so we will have specific endpoints for the madrs-s questionnaire, which madrs-s-specific "schemas"

We'll therefore need to create a mapping between our concrete madrs-s model in the API layer and our agnostic persistence model.

So we want:

- A `MadrsSSubmission`, a kind of domain object that we can serialise from the API request
- A `DiagnosticQuestionnaireSubmission` model in the persistence layer
- A `MadrsRepo` which will encapsulate the mapping between the first and the second, which we will unit test

## A note on the submission-response relationship

Really we first have a "submission" (a collection of questions specified by the particular diagnostic model, and corresponding self- or clinician-administered answers). Second, we have an individual "response" per question.

Since the nature of these kinds of diagnostic tools require all questions to be answered collectively in a single submission or session (I don't submit 5 answers now and 5 answers later), we should perhaps force the client to respect this in the way it sends the submission/response data.

I think it would be nicer for the client to send in a single API call the complete submission payload containing the answers to all the questions. This makes it easier for the server to validate the integrity of the data (this is a madrs-s submission, so it should contain 9 questions addressing X,Y,Z symptoms). It also means the submission data exists, in the persistence layer, in a binary state: either we have the records for a complete submission, or we have no records at all. There is no possibility of partially complete submissions.

There is a downside to this approach: if an end user completes a partial submission and then there is some network or other error resulting in a loss of client-side state, they would need to restart the submission. This is especially a danger for direct consumers, because we want to treat them with extreme care during a *self-administered* mental-health questionnaire. For clinicians who are submitting results on behalf of patients, this is less of a concern, although we still run the risk of annoying our partners. 

For now though let's follow the requirements of the task and, each time we write a response to an existing submission, we can just check the existing responses to validate the integrity of the incoming response. We will encapsulate this business logic in the `MadrsSSubmission` domain object mentioned above.

## Creating Submissions and Submission Responses

So we have an implementation for storing question responses, one by one, and storing them in a kind of "submission" container.

We achieve the initial objective of separating the generic/agnostic `DiagnosticQuestionnaire` persistence model from the concrete `Madrs-s` instantiation. Now we have the business logic isolated in the `madrs-self-domain.py` file - here we enforce the structure and rules of this particular diagnostic questionnaire. I'll unit tests in a follow-up push. 

This allows us to represent the madrs questionnaire in the application/domain layer so that we can add responses to it and enforce the integrity of the data before we persist anything.

There are some imperfections! For instance we treat instantiations of our domain classes as both domain objects (with no id, for example) _and_ entities (representing a persisted version of the data, with an id, for example). Also I have to pass an entire submission object in when I create a new response - I couldn't work out how best to use Django's models to manage relational writes. Anyhow, in the spirit of time I'll leave it here for now, with its warts and all :).

I'm going to figure out how to use an enum to uniquely identify responses by symptom, and then I'll add the filtering and analysis queries. I think I'll just let SQL do the heavy lifting here, and encapsulate the query, via Django's model queries, in the repo. Since we need mostly numerical analysis here, there's not much need for any domain/application logic. Onwards!

## Querying!

This was interesting. My SQL knowledge is limited and this is my first time using Django, so my repo queries are probably a little hacky! Given more time, I would write integration tests against the db for these queries to validate the query logic. It can also be nice to have computation in the application layer, so you can unit test it, but I think in this case it makes sense to let SQL do the heavy lifting and protect with int tests, especially since the Response table would very quickly contain many records.

## Solution Summary

### API layer

- I wanted to keep the interfaces slim and strict, with SRP in mind. Better to be explicit even if it means having many more handlers. Hence we have MADRS-S specific handlers, and were we to extend to other diagnostic tools, we would similarly add specific handlers for them.
- Made use of Django serialization to handle validation. Quite nice and simple to implement. Didn't go too far with restrictions - mostly just specified types.
- In a bigger application I would probably pull out the logic in the handler functions and import them into the views file. Leaving them here for simplicity's sake.

### Persistence layer

- As discussed, I have a submission-response model that is also agnostic with respect to particular instantiations of diagnostic questionnaires. This keeps the persistence model flexible if we want to support other questionnaires 
- I tried to encapsulate the models in a repo, so the models are never exposed to the API layer (I don't serialize between API request input and models). Not strictly necessary for a project of this size, but I wanted to inject between the two a domain layer to house the biz logic and protect the integrity of the submission-response data we write to the database
- I really hacked my way through the Django models ORM (first time), so I expect the code here is far from conventional. Learning!
  
### Domain layer

- This is where we encode the biz rules of particular questionnaire instantiations. We have a MadrsSubmission class which encodes the structure and rules of the questionnaire and enforces these characteristics on the data flowing through our application. Isolating the business logic here allows us to unit test it, and will help to ensure the data we write to the db is correct

### Further considerations

- A bloody linter! (Forgive me, I'm just a bit pushed for time. My eyes hurt, too)
- Integration tests on our repo methods. Especially important given we have a lot of query logic in the data layer
- Integration tests for the handler functions, with our repo (and possibly our domain objects) mocked
- Authentication + authorisation. Eventually I imagine we'd need some kind of roles-based auth, especially for the clinician platform, where we may need to support multiple accounts per clinic
- Pagination might be necessary as volumes grow, although for now we mostly fetch aggregated metrics 
- Concurrency. Load balancing might be necessary at higher volumes 
- PII - we are of course handling sensitive personal information relating to mental health. PII should therefore be at the forefront of our minds when designing any system (though I am certainly no expert in this area)
- GraphQL vs. REST. GraphQL gives you strong typing on both sides which helps with data integrity. I do like the simplicity of REST though
- Lena mentioned you currently have two clients, one for clinicians and one for "direct consumers". We might eventually build an distinct API per client, to separate concerns, and break out shared models and libraries to be consumed by both
- I realised when I started writing the summary endpoint (with scores and severity) that I should store the total_score in the Submission table. Storage is cheaper than computation and it means we can filter on this field via SQL! Doh!

### Final Words

I hope all the ramblings here weren't too annoying - I find it helps me to think, and I wanted to share the inner dialogue with you as much as possible!

Thank you guys - I enjoyed this and I really learned a lot, it was truly a Django crash course! Speak soon.

*Rusty me, navigating Django, Python, SQL, REST all at the same time:

![coder-doggo:](https://i.kym-cdn.com/photos/images/newsfeed/000/234/765/b7e.jpg)

### Setup Instructions

- Install the usual suspects: `python` (I have 3.9.6 in my venv), `django` (4.2.2) etc.
- Install project dependencies (actually, how the f do we do this? XD) 
- Create new migrations following changes to models: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Tests (from the root): `python manage.py test flow_api`
- Run server: `python manage.py runserver`

(update: oh my god, I have only just got the VSCode Python autolinting working. i have been living in the dark. i hate myself lol)