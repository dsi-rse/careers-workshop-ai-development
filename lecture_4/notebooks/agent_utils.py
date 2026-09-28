"""Agent utilities for Lecture 4: agentic resume outreach.

This module provides the agent loop machinery and LLM call helpers.
For resume loading and leaderboard submission, use resume_utils.py
(shared across all lectures).
"""

from typing import Any, Dict, Type, Union
import httpx
import json

from pydantic import BaseModel


LEADERBOARD_BASE_URL = "http://ai-leaderboard.site"

# ---------------------------------------------------------------------------
# Scoring prompt from Lecture 3 (template — fill {job_req} at runtime)
# ---------------------------------------------------------------------------

SCORING_PROMPT_TEMPLATE = """Score this resume against the job requirements below. Return a JSON object with exactly two fields: "score" (integer 0-100) and "reasoning" (1-3 sentences).

---

JOB REQUIREMENTS:
{job_req}

---

SCORING RULES — follow these exactly:

**STEP 1: Check for CORE DISQUALIFIERS (missing any = heavy penalty)**
- No C#/.NET experience → cap score at 55
- No SQL/database experience → cap score at 60
- No backend development experience at all → cap score at 60
- Less than 3 years total experience → cap score at 75

**STEP 2: Assign a BASE SCORE using these anchors**

0-30 = Completely unrelated field (e.g., nurse, teacher, accountant with no tech skills)
31-49 = Tech background but wrong domain (e.g., embedded systems, data science only, mobile-only with no web)
50-69 = Partial tech match but missing multiple core requirements (e.g., backend dev but wrong stack like Java/Python only, no .NET, no SQL)
70-79 = Significant gaps in core requirements. Use this range for:
  - Junior developer (1-3 years experience) who otherwise matches the stack
  - Frontend-only specialist (5+ years JS/React/Angular) with NO backend or .NET experience
  - Candidate with .NET experience but only 2-3 years and missing SQL or cloud
80-84 = Meets most requirements but has notable gaps (e.g., strong .NET/SQL but no frontend framework, OR strong full-stack but only 4 years experience)
85-92 = Strong match: 5+ years, has C#/.NET, SQL, at least one JS framework, Git/CI-CD. May lack AWS or microservices.
93-100 = Excellent match: 8+ years, C#/.NET, SQL Server, React or Angular, AWS, CI-CD, Agile. Matches nearly all required AND preferred qualifications.

**STEP 3: Apply BONUSES (only if base score is 50+)**
- AWS experience (EC2, S3, Lambda, RDS): +3
- Microservices architecture experience: +2
- Security knowledge (OAuth, JWT, OWASP): +2
- Testing frameworks (xUnit, NUnit, Jest): +1
- Docker/containerization: +1
- Do not exceed 100

**STEP 4: Apply PENALTIES**
- Claims skills but no evidence of use in real projects: -5
- Only 3-4 years experience (below 5-year requirement): -5
- No mention of Agile/Scrum: -2
- Frontend-only with zero backend evidence: -10 (in addition to Step 1 cap)

---

SCORING EXAMPLES to calibrate your output:

- Resume: 9 years C#/.NET, React, SQL Server, AWS, CI-CD, Agile → Score: 93-97
- Resume: 6 years C#/.NET, Angular, MySQL, Git, no AWS → Score: 85-89
- Resume: 10 years React/Angular/Vue frontend only, no .NET, no SQL → Score: 70-74
- Resume: 1.5 years experience, some C# and SQL, learning React → Score: 70-74
- Resume: 8 years Java/Spring backend, no .NET, strong SQL → Score: 50-58
- Resume: 5 years Python/Django, no .NET, no SQL Server → Score: 45-53
- Resume: Registered nurse with no software development experience → Score: 5-15

---

BE STRICT: Do not inflate scores. A frontend-only developer, no matter how experienced, must score 70-79 because they lack backend/.NET skills.
A junior developer under 3 years must score 70-79 even with the right stack.
Only candidates with 5+ years AND C#/.NET AND SQL AND a JS framework should score 85+."""


# ---------------------------------------------------------------------------
# Pydantic models for structured output
# ---------------------------------------------------------------------------

class ScoreResult(BaseModel):
    score: int
    reasoning: str


class EmailResult(BaseModel):
    email_body: str


class AgentDecision(BaseModel):
    tool: str
    parameters_json: str  # JSON string of tool parameters — parsed after validation
    reasoning: str


# ---------------------------------------------------------------------------
# LLM call helper — uses Pydantic + strict JSON schema for reliable output
# ---------------------------------------------------------------------------

def _clean_schema(obj):
    """Strip keys that OpenRouter's strict json_schema mode doesn't accept."""
    if isinstance(obj, dict):
        return {
            k: _clean_schema(v)
            for k, v in obj.items()
            if k not in ("title", "minimum", "maximum", "exclusiveMinimum",
                         "exclusiveMaximum", "default")
        }
    if isinstance(obj, list):
        return [_clean_schema(item) for item in obj]
    return obj


def structured_llm_call(
    api_key: str,
    prompt: str,
    context_data: Dict[str, Any],
    output_schema: Type[BaseModel],
    model: str = "anthropic/claude-sonnet-4-6",
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """Make a structured LLM call via OpenRouter with Pydantic strict json_schema.

    Args:
        output_schema: A Pydantic BaseModel class. The model is forced to
            return JSON matching this schema exactly (strict mode).
    """
    context_str = ""
    for key, value in context_data.items():
        if isinstance(value, str) and len(value) > 5000:
            value = value[:5000] + "\n... (truncated)"
        context_str += f"\n{key.upper()}:\n{value}\n"

    full_prompt = f"{prompt}\n{context_str}" if context_str else prompt

    schema = _clean_schema(output_schema.model_json_schema())
    schema["additionalProperties"] = False

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": temperature,
        "max_tokens": 2000,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": output_schema.__name__,
                "strict": True,
                "schema": schema,
            },
        },
    }

    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            if not content:
                return {"result": None, "error": "Empty response from model", "usage": data.get("usage", {})}
            parsed = output_schema.model_validate_json(content)
            return {"result": parsed.model_dump(), "error": None, "usage": data.get("usage", {})}
    except Exception as e:
        return {"result": None, "error": str(e), "usage": {}}


# ---------------------------------------------------------------------------
# Agent loop machinery
# ---------------------------------------------------------------------------

def _agent_decide(api_key, candidate_id, action_history, tool_registry, model, temperature=0.3):
    """Internal: agent decides which tool to call next."""
    tools_desc = "\n".join([
        f"- {name}: {info['description']}\n  Parameters: {json.dumps(info['parameters'])}"
        for name, info in tool_registry.items()
    ])

    history_str = "\n".join([
        f"Turn {i+1}: Called '{a['tool']}' -> {a['result']['message']}"
        for i, a in enumerate(action_history)
    ]) if action_history else "No actions taken yet."

    prompt = f"""You are a hiring automation agent processing candidate {candidate_id}.

AVAILABLE TOOLS:
{tools_desc}

ACTION HISTORY:
{history_str}

ROUTING RULES:
- Score >= 80 -> outcome is INTERVIEW
- Score 40-79 -> outcome is REVIEW
- Score < 40 -> outcome is REJECT

WORKFLOW:
1. First call score_resume to get the candidate's score
2. Then call draft_outreach_email with the appropriate outcome and key points from the scoring
3. Finally call done

Decide the NEXT action. You must follow the workflow order.
Return parameters_json as a JSON-encoded string of the tool parameters (e.g. '{{"candidate_id": "123"}}')."""

    result = structured_llm_call(
        api_key=api_key,
        prompt=prompt,
        context_data={},
        output_schema=AgentDecision,
        model=model,
        temperature=temperature,
    )

    # Parse parameters_json string into a dict
    decision = result["result"]
    if decision is not None:
        try:
            decision["parameters"] = json.loads(decision.pop("parameters_json"))
        except (json.JSONDecodeError, KeyError):
            decision["parameters"] = {}

    return decision, result.get("usage", {})


def run_agent(
    api_key: str,
    candidate_id: str,
    tool_registry: dict,
    model: str = "anthropic/claude-sonnet-4-6",
    temperature: float = 0.3,
    max_turns: int = 6,
    verbose: bool = True,
) -> dict:
    """Run the agent loop for one candidate.

    Returns dict with candidate_id, score, outcome, email_body,
    num_turns, and actions (full action log).
    """
    action_history = []
    total_cost = 0.0
    score = None
    outcome = None
    email_body = None

    if verbose:
        print(f"\n{'='*70}")
        print(f"  Processing: {candidate_id}")
        print(f"{'='*70}")

    for turn in range(1, max_turns + 1):
        decision, decide_usage = _agent_decide(
            api_key, candidate_id, action_history, tool_registry, model, temperature
        )
        total_cost += float(decide_usage.get("cost") or decide_usage.get("total_cost") or 0)

        if decision is None:
            if verbose:
                print(f"\n  Turn {turn}: ERROR — agent decision failed")
            break

        tool_name = decision.get("tool", "")
        params = decision.get("parameters", {})
        reasoning = decision.get("reasoning", "")

        if verbose:
            print(f"\n  Turn {turn}: {tool_name}")
            print(f"    Reasoning: {reasoning}")

        # Validate tool exists
        if tool_name not in tool_registry:
            if verbose:
                print(f"    ERROR: Unknown tool '{tool_name}'")
            break

        # Execute tool
        tool_fn = tool_registry[tool_name]["function"]
        try:
            result = tool_fn(**params)
        except Exception as e:
            result = {"status": "error", "message": str(e)}

        if verbose:
            print(f"    Result: {result['message']}")

        # Track cost from tool usage (LLM-calling tools return usage)
        tool_usage = result.get("usage", {})
        total_cost += float(tool_usage.get("cost") or tool_usage.get("total_cost") or 0)

        # Extract key outputs
        if tool_name == "score_resume" and result.get("status") == "success":
            score = result["score"]
            outcome = "INTERVIEW" if score >= 80 else ("REVIEW" if score >= 40 else "REJECT")
            if verbose:
                print(f"    -> Score: {score}, Outcome: {outcome}")

        if tool_name == "draft_outreach_email" and result.get("status") == "success":
            email_body = result["email_body"]

        # Log action
        action_history.append({
            "turn": turn,
            "tool": tool_name,
            "parameters": params,
            "reasoning": reasoning,
            "result": result,
        })

        # Check if done
        if tool_name == "done" or result.get("final"):
            break

    if verbose:
        cost_str = f"${total_cost:.4f}" if total_cost else "N/A"
        print(f"\n  Done in {len(action_history)} turns | Outcome: {outcome} | Cost: {cost_str}")
        if email_body:
            preview = email_body[:200] + ("..." if len(email_body) > 200 else "")
            print(f"\n  --- EMAIL ---\n  {preview}\n  --- END ---")

    return {
        "candidate_id": candidate_id,
        "score": score,
        "outcome": outcome,
        "email_body": email_body,
        "cost": total_cost if total_cost else None,
        "num_turns": len(action_history),
        "actions": action_history,
    }


# ---------------------------------------------------------------------------
# Lecture 4 leaderboard helpers (outreach-specific)
# ---------------------------------------------------------------------------

def submit_outreach(team_name, resume_id, outcome, email_text, score=None, cost=None, api_key="leaderboard-api-key"):
    """Submit an outreach email to the lecture 4 leaderboard."""
    url = f"{LEADERBOARD_BASE_URL}/lecture4/api/submit"
    payload = {
        "team_name": team_name,
        "resume_id": resume_id,
        "outcome": outcome,
        "email_text": email_text,
        "score": score,
        "cost": cost,
    }
    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(url, json=payload, headers={"X-API-Key": api_key})
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        return {"error": str(e)}


def delete_outreach(team_name, resume_id, api_key="leaderboard-api-key"):
    """Delete a single outreach submission."""
    url = f"{LEADERBOARD_BASE_URL}/lecture4/api/submit"
    try:
        with httpx.Client(timeout=15) as client:
            resp = client.request("DELETE", url, json={"team_name": team_name, "resume_id": resume_id}, headers={"X-API-Key": api_key})
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        return {"error": str(e)}
