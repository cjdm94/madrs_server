# flow-api

### Task

Create a server that provides an API for serving MADRS-s questions, and stores the responses (scores) of different users. The server should also be able to process and return the responses to someone analysing the data. No frontend is needed, only API endpoints.

### Requirements

- Must use Python 3 and Django: https://www.djangoproject.com/
- The MADRS-s questions should be served and responded to one-by-one.
- Endpoint that returns all users, with total score and depression severity (see below), sorted by total score and with the option to filter on a minimum and/or maximum total score.
- Endpoint that returns all users who responded a certain value on a certain question.
- Endpoint that returns the mean average score of each question.

### Good to know

- A user can simply be a username that is passed to an endpoint when necessary. No need to support creating accounts and signing in.
- There is no need to implement a client/frontend. Using cURL or whatever is good enough.
- It's good to provide a readme with instructions to make the setup and testing of the solution easier.

### JSON

[madrs-s.json](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6b2f2a7e-36e4-479a-b474-726e770ea3bc/madrs-s.json)

### About MADRS-s

MADRS-s consists of 9 self-assessment questions, where each is responded to with a "score" (integer: [0-6]). The sum of the scores represents different levels of depression according to the following scale:

- 0-12 points: No or minimal depression
- 13-19 points: Mild depression
- 20-34 points: Moderate depression
- ≥ 35 points: Severe depression

[https://en.wikipedia.org/wiki/Montgomery–Åsberg_Depression_Rating_Scale](https://en.wikipedia.org/wiki/Montgomery%E2%80%93%C3%85sberg_Depression_Rating_Scale)

[MADRS-Sjalvskattning.pdf](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6e1f893b-fecd-4ba9-87b2-3b96e43cc291/MADRS-Sjalvskattning.pdf)

Note that MADRS and MADRS-s is not exactly the same.
