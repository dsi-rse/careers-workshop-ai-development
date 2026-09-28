"""
Test harness: Run the Lecture 2 default prompts on Lecture 3 gold/silver resumes.

Checks whether the baseline prompts can discriminate gold from silver.

Usage:
    OPENROUTER_API_KEY=sk-or-... python lecture_3/test_gold_silver_scoring.py
"""

import csv
import json
import os
import sys
import time

import httpx
from pydantic import BaseModel, Field
from typing import List


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "anthropic/claude-sonnet-4-6"
CSV_PATH = "lecture_3/data/resumes_final_with_gold_silver.csv"
JOB_REQ_PATH = "lecture_3/data/job_req_senior.md"


# ---------------------------------------------------------------------------
# Schemas (from Lecture 2 notebook)
# ---------------------------------------------------------------------------

class ResumeScore(BaseModel):
    score: int
    reasoning: str


class SkillMatch(BaseModel):
    skill: str = Field(description="A skill from the resume relevant to the job requirements")
    years_experience: float = Field(description="Estimated years of experience with this skill")
    evidence: str = Field(description="Brief quote from the resume supporting this")


class SkillsExtraction(BaseModel):
    top_skills: List[SkillMatch] = Field(description="The top 3 skills most relevant to the job")
    total_years_experience: float = Field(description="Total years of professional experience")


class EducationExtraction(BaseModel):
    highest_degree: str = Field(description="Highest degree obtained")
    relevant_certifications: List[str] = Field(description="Certifications relevant to the job")
    notable_achievements: List[str] = Field(description="Up to 3 notable projects or achievements")


class FinalScore(BaseModel):
    score: int = Field(description="Overall fit score from 0-100")
    strengths: List[str] = Field(description="Top 2-3 strengths for this role")
    weaknesses: List[str] = Field(description="Top 2-3 gaps or weaknesses for this role")
    reasoning: str = Field(description="Brief overall assessment")


# ---------------------------------------------------------------------------
# API call (mirrors lecture_2/notebooks/resume_utils.py analyze_resume)
# ---------------------------------------------------------------------------

def analyze_resume(prompt, resume_text, output_schema, model=MODEL):
    schema = output_schema.model_json_schema()
    full_prompt = f"{prompt}\n\nResume:\n{resume_text[:3000]}"

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.3,
        "max_tokens": 1500,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": schema.get("title", "response"),
                "strict": True,
                "schema": schema,
            },
        },
    }

    with httpx.Client(timeout=60) as client:
        resp = client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return {"result": json.loads(content), "error": None, "usage": data.get("usage", {})}


# ---------------------------------------------------------------------------
# Scoring strategies
# ---------------------------------------------------------------------------

def score_one_shot(resume_text):
    """Lecture 2 simple one-shot prompt."""
    result = analyze_resume(
        "On a scale of 1 to 100, how good of a fit is this person for a software engineering job?",
        resume_text,
        ResumeScore,
    )
    return result["result"]["score"], result["result"]["reasoning"]


def score_multi_step(resume_text, job_req):
    """Lecture 2 multi-step prompt (extract skills, education, then score)."""
    skills = analyze_resume(
        f"Given the following job requirements, extract the top 3 most relevant skills "
        f"from the resume and estimate years of experience for each.\n\nJob Requirements:\n{job_req}",
        resume_text,
        SkillsExtraction,
    )

    edu = analyze_resume(
        f"Given the following job requirements, extract the candidate's education, "
        f"relevant certifications, and up to 3 notable achievements.\n\nJob Requirements:\n{job_req}",
        resume_text,
        EducationExtraction,
    )

    skills_summary = json.dumps(skills["result"], indent=2)
    edu_summary = json.dumps(edu["result"], indent=2)

    scoring_prompt = f"""You are scoring a resume for fit against a job posting.
Based on the extracted information below, provide a score from 0-100.

Job Requirements:
{job_req}

Extracted Skills & Experience:
{skills_summary}

Extracted Education & Achievements:
{edu_summary}

Score the candidate's overall fit. Be calibrated:
- 80-100: Strong match, meets most required qualifications
- 60-79: Decent match, meets some requirements but has gaps
- 40-59: Weak match, significant gaps in required skills
- 0-39: Poor match, missing most required qualifications"""

    final = analyze_resume(scoring_prompt, "", FinalScore)
    return final["result"]["score"], final["result"]["reasoning"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not API_KEY:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        sys.exit(1)

    # Load data
    with open(JOB_REQ_PATH, "r") as f:
        job_req = f.read()

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_resumes = {row["ID"]: row for row in reader}

    gold = {k: v for k, v in all_resumes.items() if k.startswith("g")}
    silver = {k: v for k, v in all_resumes.items() if k.startswith("s")}

    print(f"Gold resumes: {sorted(gold.keys())}")
    print(f"Silver resumes: {sorted(silver.keys())}")
    print(f"Model: {MODEL}")
    print()

    # --- Strategy 1: One-shot ---
    print("=" * 70)
    print("STRATEGY 1: One-Shot (Lecture 2 default simple prompt)")
    print("=" * 70)

    one_shot_scores = {}
    for rid in sorted(list(gold.keys()) + list(silver.keys())):
        tier = "GOLD" if rid.startswith("g") else "SILVER"
        try:
            score, reasoning = score_one_shot(all_resumes[rid]["Resume_str"])
            one_shot_scores[rid] = score
            print(f"  [{tier}] {rid}: {score:3d}/100 — {reasoning[:80]}...")
        except Exception as e:
            print(f"  [{tier}] {rid}: ERROR — {e}")
        time.sleep(0.5)

    print()

    # --- Strategy 2: Multi-step ---
    print("=" * 70)
    print("STRATEGY 2: Multi-Step (Lecture 2 extract-then-score)")
    print("=" * 70)

    multi_scores = {}
    for rid in sorted(list(gold.keys()) + list(silver.keys())):
        tier = "GOLD" if rid.startswith("g") else "SILVER"
        try:
            score, reasoning = score_multi_step(all_resumes[rid]["Resume_str"], job_req)
            multi_scores[rid] = score
            print(f"  [{tier}] {rid}: {score:3d}/100 — {reasoning[:80]}...")
        except Exception as e:
            print(f"  [{tier}] {rid}: ERROR — {e}")
        time.sleep(0.5)

    print()

    # --- Submit to leaderboard ---
    LEADERBOARD_URL = "http://ai-leaderboard.site/lecture3"
    LEADERBOARD_KEY = "leaderboard-api-key"

    for strategy_name, scores in [("one-shot", one_shot_scores), ("multi-step", multi_scores)]:
        team = f"test-{strategy_name}"
        print(f"Submitting as team '{team}' to {LEADERBOARD_URL}...")
        for rid, score in scores.items():
            try:
                with httpx.Client(timeout=10) as client:
                    resp = client.post(
                        f"{LEADERBOARD_URL}/api/submit",
                        json={"team_name": team, "resume_id": rid, "score": score},
                        headers={"X-API-Key": LEADERBOARD_KEY},
                    )
                    resp.raise_for_status()
                print(f"  {rid}: {score} -> OK")
            except Exception as e:
                print(f"  {rid}: {score} -> ERROR: {e}")
        print()

    # Check metrics from leaderboard
    print("Fetching metrics from leaderboard...")
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(f"{LEADERBOARD_URL}/api/metrics")
            resp.raise_for_status()
            metrics = resp.json()
        for m in metrics:
            print(f"  {m['team_name']}: gap={m['gold_silver_gap']}, rank_sep={m['rank_separation']}")
        print()
    except Exception as e:
        print(f"  Could not fetch metrics: {e}\n")

    # --- Summary ---
    for name, scores in [("One-Shot", one_shot_scores), ("Multi-Step", multi_scores)]:
        print("=" * 70)
        print(f"SUMMARY: {name}")
        print("=" * 70)

        g_scores = [scores[k] for k in sorted(gold.keys()) if k in scores]
        s_scores = [scores[k] for k in sorted(silver.keys()) if k in scores]

        g_mean = sum(g_scores) / len(g_scores) if g_scores else 0
        s_mean = sum(s_scores) / len(s_scores) if s_scores else 0
        gap = g_mean - s_mean

        pairs = [(g, s) for g in g_scores for s in s_scores]
        rank_sep = sum(1 for g, s in pairs if g > s) / len(pairs) if pairs else 0

        print(f"  Gold scores:   {g_scores}  mean={g_mean:.1f}")
        print(f"  Silver scores: {s_scores}  mean={s_mean:.1f}")
        print(f"  Gold-Silver gap: {gap:.1f}")
        print(f"  Rank separation: {rank_sep:.2f} (1.0 = perfect)")
        print(f"  min(gold)={min(g_scores) if g_scores else 'n/a'}, max(silver)={max(s_scores) if s_scores else 'n/a'}")
        full_sep = min(g_scores) > max(s_scores) if g_scores and s_scores else False
        print(f"  Full separation: {'YES' if full_sep else 'NO'}")
        print()


if __name__ == "__main__":
    main()
