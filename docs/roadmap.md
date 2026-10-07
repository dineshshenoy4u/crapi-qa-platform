# Roadmap: all six phases

One project, built in layers. Hours are rough estimates at your own pace. Do the phases in order; each builds on the last.

Resources named below are free documentation or articles. Search the exact title if a link has moved.

---

## Phase 1: API testing foundation (40-60 hours)

**Goal:** a Pytest framework that tests crAPI's API, including security checks.

**Learn**
- Pytest: fixtures, parametrize, markers (docs.pytest.org)
- HTTP and REST basics, status codes, JSON, auth tokens
- httpx for requests; pydantic for schema validation
- OWASP API Security Top 10 (owasp.org)
- crAPI's own challenge list in its GitHub README (OWASP/crAPI)

**Build**
- Everything in `docs/phase1-checklist.md`

**Done when**
- Clean test run, report generated, Jenkins run works, at least 3 vulnerabilities documented with `xfail(strict=True)`

**Be ready to answer:** How do fixtures differ from setup methods? What is BOLA and how would you test for it? Why assert on response shape and not just status code?

---

## Phase 2: Web UI layer (25-35 hours)

**Goal:** Playwright (Python) tests for crAPI's web interface.

**Learn**
- Playwright for Python and pytest-playwright (playwright.dev/python)
- Locators and auto-waiting (why this replaces most sleeps)
- Page object pattern
- Accessibility checks with axe

**Build**
- `tests/ui/` with page objects for login, dashboard and shop
- A test that signs up through the API, then logs in through the UI
- One accessibility scan of the main pages

**Done when**
- UI tests run headless in CI and attach a trace or screenshot on failure

**Be ready to answer:** How is Playwright's waiting different from Selenium's? How do you keep UI tests from being flaky? When should a check be an API test and not a UI test?

---

## Phase 3: Prompting and evals (40-60 hours)

**Goal:** use an LLM to generate test cases from crAPI's API description, then measure how good they are.

**Learn**
- Prompt basics and structured output (Anthropic's prompt engineering documentation)
- JSON schemas and pydantic models for model output
- What an eval is: a fixed set of inputs, a scoring rule, and a number you can compare over time
- Why LLM output varies, and how to test around that

**Build**
- `generation/`: a prompt that turns an OpenAPI-style description into test cases as JSON
- `evals/`: a small dataset and scorers (valid JSON, schema match, do generated tests run, do they catch known bugs)
- A CI step that fails when the eval score drops

**Needs:** access to an LLM API. Usage is paid but small for this project. Decide on a provider and set a spending limit before you start.

**Done when**
- Changing a prompt shows a before and after score, and CI catches a regression you introduce on purpose

**Be ready to answer:** How do you test non-deterministic output? What makes a good eval set? How did you know a prompt change was an improvement?

---

## Phase 4: RAG and context engineering (40-60 hours)

**Goal:** give the generator only the right information instead of everything.

**Learn**
- Embeddings and vector search, at the level of "what goes in, what comes out"
- Chunking, retrieval, and why retrieved text can be irrelevant
- Context windows, token budgets, and why more context can make answers worse
- Anthropic's engineering article on effective context engineering for agents

**Build**
- Index the API description, past bug notes and test results in a local vector store
- Retrieve the relevant pieces per request and build the prompt from them
- Add the same measurements from Phase 3 to compare with and without retrieval

**Done when**
- You can show eval scores with and without RAG and explain the difference

**Be ready to answer:** What does RAG fix and what does it not fix? How do you decide what goes in the context? How do you evaluate retrieval quality?

---

## Phase 5: MCP server (15-25 hours)

**Goal:** expose your framework as tools an AI client can call.

**Learn**
- What the Model Context Protocol is and what a server exposes (modelcontextprotocol.io)
- Tools, inputs and outputs, and how a client discovers them
- The MCP Python SDK

**Build**
- A small server with tools such as: list endpoints, run a test group, read the latest results
- A short README showing how to connect a client to it

**Done when**
- An MCP client can ask your server to run tests and read the results

**Be ready to answer:** What problem does MCP solve? How is a tool described to a model? What are the safety risks of giving a model tools?

---

## Phase 6: Triage agent (40-60 hours)

**Goal:** an agent that reads a failed test and decides: real bug, flaky test, or changed locator.

**Learn**
- The difference between a workflow (you define the steps) and an agent (the model chooses the steps). Anthropic's article "Building effective agents" covers this clearly
- Tool use loops, stopping conditions, and guardrails
- Evaluating an agent against labelled failures

**Build**
- An agent that uses your MCP tools to inspect failures
- A labelled set of failures (you create them on purpose) to measure accuracy
- A rule that the agent proposes changes and never applies them without approval

**Done when**
- You have a measured accuracy on your labelled set and can explain where it fails

**Be ready to answer:** Workflow or agent for this problem, and why? How do you stop an agent from looping or doing damage? How did you measure it?

---

## Stopping points

You can stop after any phase and still have something to show. Phase 3 is the first point where the project clearly shows AI skills. Update your resume at the end of each phase and describe only what is finished.
