"""FastAPI leaderboard application supporting multiple lectures."""

import csv
import math
import os
import random
from pathlib import Path

from fastapi import APIRouter, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .database import (
    LECTURE2_DB_PATH,
    LECTURE3_DB_PATH,
    LECTURE4_DB_PATH,
    add_lecture4_submission,
    add_submission,
    delete_resume_submissions,
    delete_submission,
    delete_team_submissions,
    get_all_lecture4_submissions,
    get_all_submissions,
    init_db,
    init_lecture4_db,
    reset_db,
)

API_KEY = os.environ.get("LEADERBOARD_API_KEY", "leaderboard-api-key")

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

app = FastAPI(title="Multi-Lecture Leaderboard")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Valid resume IDs per lecture (populated on startup)
LECTURE2_VALID_IDS: set[str] = set()
LECTURE3_VALID_IDS: set[str] = set()
LECTURE4_VALID_IDS: set[str] = set()
LECTURE4_GOLD_IDS: set[str] = set()
LECTURE4_SILVER_IDS: set[str] = set()

# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------


@app.on_event("startup")
def startup():
    # Lecture 2
    init_db(LECTURE2_DB_PATH)
    csv2 = REPO_ROOT / "lecture_2" / "data" / "resumes_final.csv"
    if csv2.exists():
        with open(csv2, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                LECTURE2_VALID_IDS.add(row["ID"])

    # Lecture 3
    init_db(LECTURE3_DB_PATH)
    # Try the gold/silver CSV first, fall back to plain resumes_final.csv
    csv3 = REPO_ROOT / "lecture_3" / "data" / "resumes_final_with_gold_silver.csv"
    if not csv3.exists():
        csv3 = REPO_ROOT / "lecture_3" / "data" / "resumes_final.csv"
    if csv3.exists():
        with open(csv3, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                LECTURE3_VALID_IDS.add(row["ID"])

    # Lecture 4
    init_lecture4_db(LECTURE4_DB_PATH)
    csv4 = REPO_ROOT / "lecture_4" / "data" / "resumes_final.csv"
    if csv4.exists():
        with open(csv4, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                LECTURE4_VALID_IDS.add(row["ID"])
    csv4_gs = REPO_ROOT / "lecture_4" / "data" / "resumes_final_with_gold_silver.csv"
    if csv4_gs.exists():
        with open(csv4_gs, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                LECTURE4_VALID_IDS.add(row["ID"])
                rid = row["ID"]
                if rid.startswith("g"):
                    LECTURE4_GOLD_IDS.add(rid)
                elif rid.startswith("s"):
                    LECTURE4_SILVER_IDS.add(rid)


# ---------------------------------------------------------------------------
# Auth helper
# ---------------------------------------------------------------------------


def _check_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Development Leaderboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container { text-align: center; }
        h1 { margin-bottom: 2rem; color: #1a1a2e; }
        .links { display: flex; gap: 2rem; justify-content: center; }
        a {
            display: block;
            padding: 2rem 3rem;
            background: #1a1a2e;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: 600;
            transition: background 0.2s;
        }
        a:hover { background: #16213e; }
        .desc { margin-top: 0.5rem; font-size: 0.85rem; color: #aaa; font-weight: 400; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Development Leaderboard</h1>
        <div class="links">
            <a href="/lecture2">Lecture 2<div class="desc">Resume Scoring</div></a>
            <a href="/lecture3">Lecture 3<div class="desc">Context Engineering</div></a>
            <a href="/lecture4">Lecture 4<div class="desc">Agentic Systems</div></a>
        </div>
    </div>
</body>
</html>"""


# ============================= LECTURE 2 ====================================

lecture2_router = APIRouter(prefix="/lecture2", tags=["lecture2"])


class L2SubmissionRequest(BaseModel):
    team_name: str
    resume_id: str
    score: float


class L2DeleteSubmissionRequest(BaseModel):
    team_name: str
    resume_id: str


class L2DeleteResumeRequest(BaseModel):
    resume_id: str


class L2DeleteTeamRequest(BaseModel):
    team_name: str


@lecture2_router.get("", response_class=HTMLResponse)
async def lecture2_page(request: Request):
    submissions = get_all_submissions(LECTURE2_DB_PATH)

    team_names: list[str] = []
    resume_ids: list[str] = []
    seen_teams: set[str] = set()
    seen_resumes: set[str] = set()
    grid: dict[tuple[str, str], dict] = {}

    for s in submissions:
        tid, rid = s["team_name"], s["resume_id"]
        if tid not in seen_teams:
            team_names.append(tid)
            seen_teams.add(tid)
        if rid not in seen_resumes:
            resume_ids.append(rid)
            seen_resumes.add(rid)
        grid[(rid, tid)] = {"score": s["score"], "submitted_at": s["submitted_at"]}

    team_names.sort()
    resume_ids.sort()

    return templates.TemplateResponse(
        request=request,
        name="lecture2.html",
        context={
            "team_names": team_names,
            "resume_ids": resume_ids,
            "grid": grid,
            "api_key": API_KEY,
        },
    )


@lecture2_router.post("/api/submit")
async def lecture2_submit(
    body: L2SubmissionRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    if LECTURE2_VALID_IDS and body.resume_id not in LECTURE2_VALID_IDS:
        raise HTTPException(status_code=400, detail=f"Invalid resume_id: {body.resume_id}")
    if not 0 <= body.score <= 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")
    add_submission(LECTURE2_DB_PATH, body.team_name, body.resume_id, body.score)
    return {"status": "ok", "team_name": body.team_name, "resume_id": body.resume_id, "score": body.score}


@lecture2_router.delete("/api/submit")
async def lecture2_delete_submission(
    body: L2DeleteSubmissionRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_submission(LECTURE2_DB_PATH, body.team_name, body.resume_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"status": "ok", "team_name": body.team_name, "resume_id": body.resume_id, "deleted": deleted}


@lecture2_router.post("/api/delete_team")
async def lecture2_delete_team(
    body: L2DeleteTeamRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_team_submissions(LECTURE2_DB_PATH, body.team_name)
    return {"status": "ok", "team_name": body.team_name, "deleted": deleted}


@lecture2_router.post("/api/delete_resume")
async def lecture2_delete_resume(
    body: L2DeleteResumeRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_resume_submissions(LECTURE2_DB_PATH, body.resume_id)
    return {"status": "ok", "resume_id": body.resume_id, "deleted": deleted}


@lecture2_router.post("/api/reset")
async def lecture2_reset(x_api_key: str | None = Header(default=None)):
    _check_api_key(x_api_key)
    reset_db(LECTURE2_DB_PATH)
    return {"status": "ok", "message": "Leaderboard reset"}


@lecture2_router.get("/api/submissions")
async def lecture2_submissions():
    return get_all_submissions(LECTURE2_DB_PATH)


@lecture2_router.get("/api/health")
async def lecture2_health():
    return {"status": "healthy"}


@lecture2_router.post("/api/seed")
async def lecture2_seed(x_api_key: str | None = Header(default=None)):
    """Seed the database with test data: 15 teams x 10 resume IDs."""
    _check_api_key(x_api_key)
    teams = [f"Team {name}" for name in [
        "Alpha", "Beta", "Gamma", "Delta", "Epsilon",
        "Zeta", "Eta", "Theta", "Iota", "Kappa",
        "Lambda", "Mu", "Nu", "Xi", "Omicron",
    ]]
    resume_ids = (
        sorted(random.sample(list(LECTURE2_VALID_IDS), 10))
        if len(LECTURE2_VALID_IDS) >= 10
        else [str(i) for i in range(10)]
    )
    for team in teams:
        for rid in resume_ids:
            score = round(random.uniform(30, 99), 1)
            add_submission(LECTURE2_DB_PATH, team, rid, score)
    return {"status": "ok", "teams": len(teams), "resumes": len(resume_ids)}


# ============================= LECTURE 3 ====================================

lecture3_router = APIRouter(prefix="/lecture3", tags=["lecture3"])


class L3SubmissionRequest(BaseModel):
    team_name: str
    resume_id: str
    score: float
    cost: float | None = None


class L3DeleteSubmissionRequest(BaseModel):
    team_name: str
    resume_id: str


class L3DeleteResumeRequest(BaseModel):
    resume_id: str


class L3DeleteTeamRequest(BaseModel):
    team_name: str


def _classify_id(resume_id: str) -> str:
    """Return 'gold', 'silver', or 'wild' based on the ID prefix."""
    if resume_id.startswith("g"):
        return "gold"
    elif resume_id.startswith("s"):
        return "silver"
    else:
        return "wild"


def _compute_metrics(submissions: list[dict], team_name: str) -> dict:
    """Compute ordinal metrics for a given team."""
    relevant = [s for s in submissions if s["team_name"] == team_name]

    gold_scores: list[float] = []
    silver_scores: list[float] = []
    wild_scores: list[float] = []

    for s in relevant:
        cat = _classify_id(s["resume_id"])
        if cat == "gold":
            gold_scores.append(s["score"])
        elif cat == "silver":
            silver_scores.append(s["score"])
        else:
            wild_scores.append(s["score"])

    def mean(vals: list[float]) -> float | None:
        return sum(vals) / len(vals) if vals else None

    def std(vals: list[float]) -> float | None:
        if len(vals) < 2:
            return None
        m = sum(vals) / len(vals)
        variance = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
        return math.sqrt(variance)

    gold_mean = mean(gold_scores)
    silver_mean = mean(silver_scores)
    wild_mean = mean(wild_scores)

    # Rank separation: fraction of (g, s) pairs where score(g) > score(s)
    rank_separation: float | None = None
    if gold_scores and silver_scores:
        pairs = 0
        wins = 0
        for g in gold_scores:
            for sv in silver_scores:
                pairs += 1
                if g > sv:
                    wins += 1
        rank_separation = wins / pairs if pairs > 0 else None

    return {
        "team_name": team_name,
        "gold_mean": round(gold_mean, 4) if gold_mean is not None else None,
        "silver_mean": round(silver_mean, 4) if silver_mean is not None else None,
        "wild_mean": round(wild_mean, 4) if wild_mean is not None else None,
        "gold_silver_gap": round(gold_mean - silver_mean, 4) if gold_mean is not None and silver_mean is not None else None,
        "gold_wild_gap": round(gold_mean - wild_mean, 4) if gold_mean is not None and wild_mean is not None else None,
        "rank_separation": round(rank_separation, 4) if rank_separation is not None else None,
        "gold_std": round(std(gold_scores), 4) if std(gold_scores) is not None else None,
        "silver_std": round(std(silver_scores), 4) if std(silver_scores) is not None else None,
        "num_gold": len(gold_scores),
        "num_silver": len(silver_scores),
        "num_wild": len(wild_scores),
    }


@lecture3_router.get("", response_class=HTMLResponse)
async def lecture3_page(request: Request):
    submissions = get_all_submissions(LECTURE3_DB_PATH)

    team_names: list[str] = []
    resume_ids: list[str] = []
    seen_teams: set[str] = set()
    seen_resumes: set[str] = set()
    grid: dict[tuple[str, str], dict] = {}

    for s in submissions:
        tid, rid = s["team_name"], s["resume_id"]
        if tid not in seen_teams:
            team_names.append(tid)
            seen_teams.add(tid)
        if rid not in seen_resumes:
            resume_ids.append(rid)
            seen_resumes.add(rid)
        grid[(rid, tid)] = {"score": s["score"], "submitted_at": s["submitted_at"], "cost": s.get("cost")}

    team_names.sort()
    # Sort resume IDs: gold first, then silver, then wild (numeric)
    def _rid_sort_key(rid: str) -> tuple[int, str]:
        if rid.startswith("g"):
            return (0, rid)
        elif rid.startswith("s"):
            return (1, rid)
        else:
            return (2, rid)

    resume_ids.sort(key=_rid_sort_key)

    return templates.TemplateResponse(
        request=request,
        name="lecture3.html",
        context={
            "team_names": team_names,
            "resume_ids": resume_ids,
            "grid": grid,
            "api_key": API_KEY,
        },
    )


@lecture3_router.post("/api/submit")
async def lecture3_submit(
    body: L3SubmissionRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    if LECTURE3_VALID_IDS and body.resume_id not in LECTURE3_VALID_IDS:
        raise HTTPException(status_code=400, detail=f"Invalid resume_id: {body.resume_id}")
    if not 0 <= body.score <= 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")
    add_submission(LECTURE3_DB_PATH, body.team_name, body.resume_id, body.score, cost=body.cost)
    return {
        "status": "ok",
        "team_name": body.team_name,
        "resume_id": body.resume_id,
        "score": body.score,
        "cost": body.cost,
    }


@lecture3_router.delete("/api/submit")
async def lecture3_delete_submission(
    body: L3DeleteSubmissionRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_submission(LECTURE3_DB_PATH, body.team_name, body.resume_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {
        "status": "ok",
        "team_name": body.team_name,
        "resume_id": body.resume_id,
        "deleted": deleted,
    }


@lecture3_router.post("/api/delete_team")
async def lecture3_delete_team(
    body: L3DeleteTeamRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_team_submissions(LECTURE3_DB_PATH, body.team_name)
    return {"status": "ok", "team_name": body.team_name, "deleted": deleted}


@lecture3_router.post("/api/delete_resume")
async def lecture3_delete_resume(
    body: L3DeleteResumeRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_resume_submissions(LECTURE3_DB_PATH, body.resume_id)
    return {"status": "ok", "resume_id": body.resume_id, "deleted": deleted}


@lecture3_router.post("/api/reset")
async def lecture3_reset(x_api_key: str | None = Header(default=None)):
    _check_api_key(x_api_key)
    reset_db(LECTURE3_DB_PATH)
    return {"status": "ok", "message": "Lecture 3 leaderboard reset"}


@lecture3_router.get("/api/submissions")
async def lecture3_submissions():
    return get_all_submissions(LECTURE3_DB_PATH)


@lecture3_router.get("/api/health")
async def lecture3_health():
    return {"status": "healthy"}


@lecture3_router.get("/api/metrics")
async def lecture3_metrics(team: str | None = None):
    """Compute metrics for all teams or a specific team."""
    submissions = get_all_submissions(LECTURE3_DB_PATH)

    # Collect unique teams
    team_names: set[str] = set()
    for s in submissions:
        team_names.add(s["team_name"])

    results = []
    for t in sorted(team_names):
        if team is not None and t != team:
            continue
        results.append(_compute_metrics(submissions, t))

    return results


@lecture3_router.post("/api/seed")
async def lecture3_seed(x_api_key: str | None = Header(default=None)):
    """Seed the database with test data: 15 teams x 10 resume IDs with gold/silver/wild."""
    _check_api_key(x_api_key)
    teams = [f"Team {name}" for name in [
        "Alpha", "Beta", "Gamma", "Delta", "Epsilon",
        "Zeta", "Eta", "Theta", "Iota", "Kappa",
        "Lambda", "Mu", "Nu", "Xi", "Omicron",
    ]]
    # Pick gold, silver, and wild IDs
    gold_ids = sorted(random.sample([r for r in LECTURE3_VALID_IDS if r.startswith("g")], min(3, len([r for r in LECTURE3_VALID_IDS if r.startswith("g")]))))
    silver_ids = sorted(random.sample([r for r in LECTURE3_VALID_IDS if r.startswith("s")], min(3, len([r for r in LECTURE3_VALID_IDS if r.startswith("s")]))))
    wild_ids = sorted(random.sample([r for r in LECTURE3_VALID_IDS if not r.startswith("g") and not r.startswith("s")], min(4, len([r for r in LECTURE3_VALID_IDS if not r.startswith("g") and not r.startswith("s")]))))
    resume_ids = gold_ids + silver_ids + wild_ids
    if not resume_ids:
        resume_ids = ["g01", "g02", "g03", "s01", "s02", "s03", "10089434", "10247517", "10265057", "10840430"]
    for team in teams:
        for rid in resume_ids:
            if rid.startswith("g"):
                score = round(random.uniform(70, 99), 1)
            elif rid.startswith("s"):
                score = round(random.uniform(10, 45), 1)
            else:
                score = round(random.uniform(30, 70), 1)
            cost = round(random.uniform(0.001, 0.01), 5)
            add_submission(LECTURE3_DB_PATH, team, rid, score, cost=cost)
    return {"status": "ok", "teams": len(teams), "resumes": len(resume_ids)}


# ============================= LECTURE 4 ====================================

lecture4_router = APIRouter(prefix="/lecture4", tags=["lecture4"])

VALID_OUTCOMES = {"INTERVIEW", "REJECT", "REVIEW"}


class L4SubmissionRequest(BaseModel):
    team_name: str
    resume_id: str
    outcome: str  # INTERVIEW, REJECT, or REVIEW
    email_text: str
    score: float | None = None
    cost: float | None = None


class L4DeleteSubmissionRequest(BaseModel):
    team_name: str
    resume_id: str


class L4DeleteTeamRequest(BaseModel):
    team_name: str


class L4DeleteResumeRequest(BaseModel):
    resume_id: str


@lecture4_router.get("", response_class=HTMLResponse)
async def lecture4_page(request: Request):
    submissions = get_all_lecture4_submissions(LECTURE4_DB_PATH)

    team_names: list[str] = []
    resume_ids: list[str] = []
    seen_teams: set[str] = set()
    seen_resumes: set[str] = set()
    grid: dict[tuple[str, str], dict] = {}

    for s in submissions:
        tid, rid = s["team_name"], s["resume_id"]
        if tid not in seen_teams:
            team_names.append(tid)
            seen_teams.add(tid)
        if rid not in seen_resumes:
            resume_ids.append(rid)
            seen_resumes.add(rid)
        grid[(rid, tid)] = {
            "outcome": s["outcome"],
            "email_text": s["email_text"],
            "score": s.get("score"),
            "cost": s.get("cost"),
            "submitted_at": s.get("submitted_at"),
        }

    team_names.sort()

    # Sort resume IDs: gold first, then silver, then wild (alphabetic within tier)
    def _rid_sort_key(rid: str) -> tuple[int, str]:
        if rid.startswith("g"):
            return (0, rid)
        elif rid.startswith("s"):
            return (1, rid)
        else:
            return (2, rid)

    resume_ids.sort(key=_rid_sort_key)

    # Build email_data for the slideshow view
    email_data: dict[str, list[dict]] = {}
    for (rid, tn), info in grid.items():
        email_data.setdefault(rid, []).append({
            "team_name": tn,
            "outcome": info["outcome"],
            "email_text": info["email_text"],
            "score": info.get("score"),
            "cost": info.get("cost"),
            "submitted_at": info.get("submitted_at"),
        })

    return templates.TemplateResponse(
        request=request,
        name="lecture4.html",
        context={
            "team_names": team_names,
            "resume_ids": resume_ids,
            "grid": grid,
            "api_key": API_KEY,
            "email_data": email_data,
        },
    )


@lecture4_router.post("/api/submit")
async def lecture4_submit(
    body: L4SubmissionRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    if LECTURE4_VALID_IDS and body.resume_id not in LECTURE4_VALID_IDS:
        raise HTTPException(status_code=400, detail=f"Invalid resume_id: {body.resume_id}")
    if body.outcome not in VALID_OUTCOMES:
        raise HTTPException(status_code=400, detail=f"Invalid outcome: {body.outcome}. Must be one of: INTERVIEW, REJECT, REVIEW")
    add_lecture4_submission(
        LECTURE4_DB_PATH, body.team_name, body.resume_id, body.outcome,
        body.email_text, score=body.score, cost=body.cost,
    )
    return {
        "status": "ok",
        "team_name": body.team_name,
        "resume_id": body.resume_id,
        "outcome": body.outcome,
        "score": body.score,
        "cost": body.cost,
    }


@lecture4_router.delete("/api/submit")
async def lecture4_delete_submission(
    body: L4DeleteSubmissionRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_submission(LECTURE4_DB_PATH, body.team_name, body.resume_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {
        "status": "ok",
        "team_name": body.team_name,
        "resume_id": body.resume_id,
        "deleted": deleted,
    }


@lecture4_router.post("/api/delete_team")
async def lecture4_delete_team(
    body: L4DeleteTeamRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_team_submissions(LECTURE4_DB_PATH, body.team_name)
    return {"status": "ok", "team_name": body.team_name, "deleted": deleted}


@lecture4_router.post("/api/delete_resume")
async def lecture4_delete_resume(
    body: L4DeleteResumeRequest, x_api_key: str | None = Header(default=None)
):
    _check_api_key(x_api_key)
    deleted = delete_resume_submissions(LECTURE4_DB_PATH, body.resume_id)
    return {"status": "ok", "resume_id": body.resume_id, "deleted": deleted}


@lecture4_router.post("/api/reset")
async def lecture4_reset(x_api_key: str | None = Header(default=None)):
    _check_api_key(x_api_key)
    reset_db(LECTURE4_DB_PATH)
    return {"status": "ok", "message": "Lecture 4 leaderboard reset"}


@lecture4_router.get("/api/submissions")
async def lecture4_submissions():
    return get_all_lecture4_submissions(LECTURE4_DB_PATH)


@lecture4_router.get("/api/health")
async def lecture4_health():
    return {"status": "healthy"}


@lecture4_router.post("/api/seed")
async def lecture4_seed(x_api_key: str | None = Header(default=None)):
    """Seed the database with test data: 15 teams x 8 resume IDs with outcomes."""
    _check_api_key(x_api_key)

    teams = [f"Team {name}" for name in [
        "Alpha", "Beta", "Gamma", "Delta", "Epsilon",
        "Zeta", "Eta", "Theta", "Iota", "Kappa",
        "Lambda", "Mu", "Nu", "Xi", "Omicron",
    ]]

    resume_ids = ["g01", "g02", "s01", "s02", "10840430", "16899268", "24083609", "25990239"]

    interview_emails = [
        "We were impressed by your experience and would like to invite you to a technical interview. Our team will reach out to schedule a time.",
        "Your background is an excellent match for this role. We'd love to move forward with a technical assessment.",
        "After reviewing your application, we're confident you'd be a strong addition. Let's set up an interview.",
    ]
    reject_emails = [
        "After careful consideration, we've decided to move forward with candidates whose experience more closely aligns with our needs.",
        "We appreciate your interest but have decided to pursue other candidates at this time.",
        "Thank you for applying. Unfortunately, we won't be moving forward with your candidacy.",
    ]
    review_emails = [
        "Your application has been flagged for additional review by our hiring committee. You should hear back within a week.",
        "We're reviewing your application in more detail. Our senior engineers will evaluate your candidacy this week.",
    ]

    count = 0
    for team in teams:
        num_resumes = random.randint(len(resume_ids) * 6 // 10, len(resume_ids))
        selected = random.sample(resume_ids, num_resumes)
        for rid in selected:
            if rid.startswith("g"):
                outcome = random.choices(["INTERVIEW", "REVIEW", "REJECT"], weights=[75, 20, 5])[0]
                score = random.randint(78, 98)
            elif rid.startswith("s"):
                outcome = random.choices(["REJECT", "REVIEW", "INTERVIEW"], weights=[65, 25, 10])[0]
                score = random.randint(30, 72)
            else:
                outcome = random.choices(["REJECT", "REVIEW", "INTERVIEW"], weights=[50, 30, 20])[0]
                score = random.randint(5, 55)

            if outcome == "INTERVIEW":
                email = random.choice(interview_emails)
            elif outcome == "REJECT":
                email = random.choice(reject_emails)
            else:
                email = random.choice(review_emails)

            email = f"Re: Application #{rid}\n\n{email}"
            cost = round(random.uniform(0.001, 0.015), 5)

            add_lecture4_submission(
                LECTURE4_DB_PATH, team, rid, outcome, email,
                score=score, cost=cost,
            )
            count += 1

    return {"status": "ok", "teams": len(teams), "submissions": count}


# ---------------------------------------------------------------------------
# Mount routers
# ---------------------------------------------------------------------------
app.include_router(lecture2_router)
app.include_router(lecture3_router)
app.include_router(lecture4_router)
