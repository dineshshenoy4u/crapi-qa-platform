# crAPI QA Platform

Python and Pytest test framework for [OWASP crAPI](https://github.com/OWASP/crAPI), an intentionally vulnerable API. This is Phase 1 of a larger project (later phases add Playwright UI tests, LLM-assisted test generation with evals, RAG, an MCP server and a triage agent).

New here? Read `START_HERE.md` first, then `docs/roadmap.md` for all six phases.

## Layout

```
framework/      config, API client, test data helpers
tests/api/      smoke, auth, negative, contract tests
tests/security/ OWASP API Top 10 style checks
docs/           Docker setup and the Phase 1 checklist
Jenkinsfile     skeleton CI pipeline
```

## Quick start

1. Install Docker and start crAPI: see `docs/docker-setup.md`
2. Create a virtual environment and install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
```

3. Run the tests:

```
pytest                           # everything
pytest -m smoke                  # quick check that the app and core endpoints respond
pytest tests/security            # security checks
pytest --html=reports/report.html --self-contained-html
```

If crAPI isn't running, the run is skipped with a message telling you to start it.

## What is implemented vs what is yours to write

Implemented: client, fixtures, smoke tests, basic auth tests, one schema test.
Left for you: every test marked `TODO (you)`. Follow `docs/phase1-checklist.md`.

## Safety

crAPI is vulnerable on purpose. Run it and these tests only against your own local instance.
