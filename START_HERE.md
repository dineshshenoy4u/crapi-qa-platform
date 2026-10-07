# Start here

This project is a learning path. You are not meant to write everything at once. Each phase teaches one group of skills, and every phase ends with something you can run and explain.

## Your first day (about 3 hours)

Do these in order and stop when you finish. Do not read ahead.

1. **Install Docker** and confirm `docker run hello-world` works. Steps: `docs/docker-setup.md`
2. **Start crAPI** with the commands in the same file. Open http://localhost:8888 and sign up for an account. Click around: log in, open the dashboard, browse the shop.
3. **Watch the API calls.** Open your browser's developer tools (F12), go to the Network tab, and repeat the signup and login. Look at the requests: the URL, the method, the JSON body, the response. This is what your tests will automate.
4. **Set up Python.** Create a virtual environment and install requirements (README quick start).
5. **Run the smoke tests:** `pytest -m smoke`. If a test fails, that is useful: compare the endpoint path or response shape with what you saw in the Network tab and fix `framework/api_client.py`.

If you finish step 5 with passing smoke tests, Day 1 is a success.

## Week 1 plan (about 5 hours a day)

| Day | Focus | End of day you have |
|---|---|---|
| 1 | Docker, crAPI, Network tab, smoke tests | App running, smoke tests passing |
| 2 | Read the framework files line by line | Can explain `api_client.py` and `conftest.py` in your own words |
| 3 | Auth tests: write the two TODO tests in `test_auth.py` | Two new passing tests |
| 4 | Negative tests: missing fields with `parametrize` | A parametrized test running many cases |
| 5 | Negative tests: invalid values and boundaries | Written list of limits you discovered |
| 6 | Contract test: Product schema with pydantic | Schema test passing |
| 7 | Review, clean up, first Git commit and GitHub push | A repo with a README and history |

## How to learn with this project

- **Try first, then ask.** Spend 15-20 minutes on a problem before asking for help. When you ask, paste the error and what you tried.
- **Ask for explanations, not just answers.** "Explain this line" and "why is it written this way" are better questions than "write this for me".
- **Commit at the end of every session.** Small commits with clear messages show how you work.
- **Keep a notes file.** One line per thing you learned or got stuck on. It becomes your interview material.

## Where everything is

- `docs/roadmap.md`: all six phases, what to learn, what to build, and how to know each is done
- `docs/phase1-checklist.md`: the detailed Phase 1 task list
- `docs/docker-setup.md`: Docker and crAPI setup
- `README.md`: how to run the tests
