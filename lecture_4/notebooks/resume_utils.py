"""Utility functions for resume screening with LLMs."""

from typing import Any, Dict, Type
import httpx
import json
import csv
import time

from pydantic import BaseModel

LEADERBOARD_BASE_URL = "http://ai-leaderboard.site"


def load_resumes(csv_path: str) -> Dict[str, Dict[str, str]]:
    """Load all resumes from CSV into a dictionary keyed by ID."""
    resumes = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            resumes[row['ID']] = {
                'ID': row['ID'],
                'Resume_str': row['Resume_str'],
                'Resume_html': row['Resume_html']
            }
    return resumes


def load_job_requirements(file_path: str) -> str:
    """Load job requirements from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def analyze_resume(
    api_key: str,
    prompt: str,
    resume_text: str,
    output_schema: Type[BaseModel],
    model: str = "anthropic/claude-sonnet-4-6",
    temperature: float = 0.3
) -> Dict[str, Any]:
    """
    Analyze a resume using an LLM with structured output.

    Args:
        api_key: OpenRouter API key
        prompt: The instruction for what to analyze
        resume_text: The resume text to analyze
        output_schema: A Pydantic BaseModel class defining the output structure
        model: Model to use
        temperature: Sampling temperature (default: 0.3 for consistency)

    Returns:
        Dict with 'result' (parsed JSON), 'error' (if any), 'usage' (token counts), and 'cost'
    """
    schema = output_schema.model_json_schema()

    # Strip keys that OpenRouter's strict json_schema mode doesn't accept
    def _clean_schema(obj):
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

    schema = _clean_schema(schema)
    schema["additionalProperties"] = False

    full_prompt = f"""{prompt}

Resume:
{resume_text[:3000]}"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": temperature,
        "max_tokens": 1500,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": output_schema.__name__,
                "strict": True,
                "schema": schema,
            },
        },
    }

    max_retries = 3
    backoff = 2  # seconds

    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=60) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()

                if "error" in data:
                    return {
                        "result": None,
                        "error": f"API error: {data['error']}",
                        "usage": {},
                        "cost": None,
                    }

                content = data["choices"][0]["message"]["content"]
                if not content:
                    return {
                        "result": None,
                        "error": f"Empty response from model. Raw response: {data}",
                        "usage": data.get("usage", {}),
                        "cost": None,
                    }

                parsed = output_schema.model_validate_json(content)

                usage = data.get("usage", {})
                cost = usage.get("cost")

                return {
                    "result": parsed.model_dump(),
                    "error": None,
                    "usage": usage,
                    "cost": cost,
                }
        except (httpx.HTTPStatusError, httpx.ConnectError, httpx.ReadTimeout) as e:
            status = getattr(e, "response", None)
            status_code = status.status_code if status is not None else None
            if status_code in (502, 503, 429) or status_code is None:
                if attempt < max_retries - 1:
                    wait = backoff * (attempt + 1)
                    print(f"  [retry {attempt + 1}/{max_retries}] {status_code or type(e).__name__}, waiting {wait}s...")
                    time.sleep(wait)
                    continue
            return {
                "result": None,
                "error": str(e),
                "usage": {},
                "cost": None,
            }
        except Exception as e:
            return {
                "result": None,
                "error": str(e),
                "usage": {},
                "cost": None,
            }

    return {
        "result": None,
        "error": f"Failed after {max_retries} retries",
        "usage": {},
        "cost": None,
    }


def submit_score(
    team_name: str,
    resume_id: str,
    score: float,
    lecture: int = 4,
    cost: float | None = None,
    api_key: str = "leaderboard-api-key",
) -> dict:
    """Submit a resume score to the leaderboard.

    Args:
        team_name: Your team's name
        resume_id: The resume ID being scored
        score: Score from 0-100
        lecture: Which lecture leaderboard to submit to (2, 3, or 4)
        cost: Optional cost of the API call(s)
        api_key: API key for authentication
    """
    api_url = f"{LEADERBOARD_BASE_URL}/lecture{lecture}"
    payload = {"team_name": team_name, "resume_id": str(resume_id), "score": score}
    if cost is not None:
        payload["cost"] = cost
    with httpx.Client(timeout=10) as client:
        resp = client.post(
            f"{api_url}/api/submit",
            json=payload,
            headers={"X-API-Key": api_key},
        )
        resp.raise_for_status()
        return resp.json()


def delete_score(
    team_name: str,
    resume_id: str,
    lecture: int = 4,
    api_key: str = "leaderboard-api-key",
) -> dict:
    """Delete a single submission from the leaderboard."""
    api_url = f"{LEADERBOARD_BASE_URL}/lecture{lecture}"
    with httpx.Client(timeout=10) as client:
        resp = client.request(
            "DELETE",
            f"{api_url}/api/submit",
            json={"team_name": team_name, "resume_id": str(resume_id)},
            headers={"X-API-Key": api_key},
        )
        resp.raise_for_status()
        return resp.json()


def delete_team(
    team_name: str,
    lecture: int = 4,
    api_key: str = "leaderboard-api-key",
) -> dict:
    """Delete all submissions for a team from the leaderboard."""
    api_url = f"{LEADERBOARD_BASE_URL}/lecture{lecture}"
    with httpx.Client(timeout=10) as client:
        resp = client.post(
            f"{api_url}/api/delete_team",
            json={"team_name": team_name},
            headers={"X-API-Key": api_key},
        )
        resp.raise_for_status()
        return resp.json()
