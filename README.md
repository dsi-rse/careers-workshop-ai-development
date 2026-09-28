# 2026-AI-Development
Winter 2026 AI Development Training Series

This course was developed in partnership between the University of Chicago's [Career Advancement Office](https://careeradvancement.uchicago.edu/) and the University of Chicago's [Data Science Institute](https://datascience.uchicago.edu/).


## Workshop: AI Development (4-part series)

This repository contains materials for a four-part workshop on AI development for advanced undergraduates (3rd/4th year).

### Lecture 1: Foundations
[Slides](lecture_1/slides/lecture_1.pdf)
- What LLMs are, how they work (tokens, context windows, temperature), and what they cost
- Hands-on with the OpenRouter API: sending your first programmatic LLM call
- Understanding the gap between "chatbot" and "AI-powered application"

**Readings for Lecture 2:**
- [A Survey of AI Coding](https://paulgp.com/ai-coding/2025/12/02/ai-coding.html)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic's guide to designing context windows
- [Context Engineering](https://simonwillison.net/2025/Jun/27/context-engineering/) — Simon Willison's take
- [Agent Best Practices](https://cursor.com/blog/agent-best-practices) — Cursor's guide to context engineering
- [Welcome to Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) — LONG, only read as long as you are interested!
- [Why ChatGPT Can't Be Trusted](https://garymarcus.substack.com/p/why-chatgpt-cant-be-trusted-with), [Breaking: Marcus Weighs In](https://garymarcus.substack.com/p/breaking-marcus-weighs-in-mostly), [Let's Be Honest](https://garymarcus.substack.com/p/lets-be-honest-generative-ai-isnt) — Gary Marcus on AI limitations
- [Claude Code Unpacked](https://ccunpacked.dev/)


### Lecture 2: Building a System
[Slides](lecture_2/slides/lecture_2.pdf)
- From idea to working prototype: vertical slices, MVPs, and the Crawl-Walk-Run framework
- Build a resume screening pipeline — one prompt that scores 130 resumes against a job description
- Understanding costs, latency, and model selection trade-offs in production

**Readings for Lecture 3:**
- [Horizontal Slice vs Vertical Slice Programming](https://victormagalhaes-dev.medium.com/comparing-approaches-horizontal-slice-vs-vertical-slice-programming-d8db017952e4)
- [AI Unit of Work](https://blog.nilenso.com/blog/2025/09/15/ai-unit-of-work/) — How to scope work for AI systems
- [AI Blindspots](https://ezyang.github.io/ai-blindspots/) — Where AI agents fail and how to design around it
- [Scaling Agents](https://cursor.com/blog/scaling-agents) — Cursor's insights on production-grade AI agents


### Lecture 3: Making It Good
[Slides](lecture_3/slides/lecture_3.pdf)
- Context engineering techniques that reliably improve LLM output: decomposition, grounding with citations, and few-shot examples
- Iterate on the Lecture 2 resume scorer until gold and silver candidates separate cleanly
- Learn why a well-engineered prompt can make even cheap models perform well

**Readings for Lecture 4:**
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic's guide to agent patterns and best practices


### Lecture 4: AI Agents & Tool Use
[Slides](lecture_4/slides/lecture_4.pdf)
- Move from generating text to taking action: give LLMs tools that interact with the real world
- Build an agentic email outreach system — the agent scores resumes, decides outcomes, and drafts personalized emails
- Production considerations: failure modes, safety guardrails, ethical implications, and human-in-the-loop design

## Running notebooks (per lecture) 

Each lecture directory contains a `Makefile`, `Dockerfile`, and `pyproject.toml`.

From a lecture directory (e.g. `lecture_2/`):
- `make build`
- `make notebook` (starts Jupyter in Docker on port 8888)
- `make interactive` (drops you into a bash shell in the container)

