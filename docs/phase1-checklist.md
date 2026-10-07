# Phase 1 checklist

Work top to bottom. Each item is a skipped test or a small framework task. Remove the `skip` marker, write the test, run it.

## Framework (you own this)
- [ ] Read `framework/api_client.py` and `tests/conftest.py` until you can explain every line
- [ ] Verify each endpoint path in `api_client.py` against your running crAPI (browser dev tools, Network tab)
- [ ] Add a method to the client for one more endpoint of your choice
- [ ] Add a response-time assertion helper (for example, fail if slower than a threshold you pick)
- [ ] Add logging of request and response on failure

## API tests
- [ ] `tests/api/test_auth.py`: duplicate signup, unknown user login
- [ ] `tests/api/test_negative.py`: missing fields (parametrized), invalid values, boundaries, bad query params
- [ ] `tests/api/test_contract.py`: Product schema with pydantic

## Security tests (against your own local crAPI only)
- [ ] BOLA: two users, cross-access
- [ ] Brute-force / rate limiting on login
- [ ] Excessive data exposure in responses
- [ ] Oversized payload handling
- [ ] Mass assignment
- [ ] For each confirmed vulnerability, mark the test `xfail(strict=True, reason="...")` and write one line on the risk

## Reporting and CI
- [ ] Generate the HTML report: `pytest --html=reports/report.html --self-contained-html`
- [ ] Get the Jenkinsfile running on a local Jenkins and publish the report

## Done when
- [ ] Clean `pytest` run on a fresh crAPI with no skipped tests except documented known vulnerabilities
- [ ] README explains how to run it, what is covered, and what vulnerabilities you found
