"""SQLite database helpers for the leaderboard (supports lecture 2 and lecture 3)."""

import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LECTURE2_DB_PATH = REPO_ROOT / "leaderboard" / "leaderboard_lecture2.db"
LECTURE3_DB_PATH = REPO_ROOT / "leaderboard" / "leaderboard_lecture3.db"


# ---------------------------------------------------------------------------
# Lecture 2 helpers (no strategy column – same schema as original)
# ---------------------------------------------------------------------------

def init_db(db_path: Path) -> None:
    """Create the submissions table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            team_name TEXT NOT NULL,
            resume_id TEXT NOT NULL,
            score REAL NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(team_name, resume_id)
        )
        """
    )
    # Add cost column if it doesn't exist (migration for existing DBs)
    try:
        conn.execute("ALTER TABLE submissions ADD COLUMN cost REAL")
    except sqlite3.OperationalError:
        pass  # column already exists
    conn.commit()
    conn.close()


def add_submission(
    db_path: Path, team_name: str, resume_id: str, score: float,
    cost: float | None = None,
) -> None:
    """Insert or replace a submission."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        INSERT OR REPLACE INTO submissions (team_name, resume_id, score, submitted_at, cost)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
        """,
        (team_name, resume_id, score, cost),
    )
    conn.commit()
    conn.close()


def get_all_submissions(db_path: Path) -> list[dict]:
    """Return all submissions as a list of dicts (lecture 2)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT team_name, resume_id, score, submitted_at, cost FROM submissions "
        "ORDER BY submitted_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_submission(db_path: Path, team_name: str, resume_id: str) -> int:
    """Delete a single submission (lecture 2). Returns number of rows deleted."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "DELETE FROM submissions WHERE team_name = ? AND resume_id = ?",
        (team_name, resume_id),
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted


def delete_team_submissions(db_path: Path, team_name: str) -> int:
    """Delete all submissions for a given team (lecture 2). Returns number of rows deleted."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "DELETE FROM submissions WHERE team_name = ?", (team_name,)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted


def delete_resume_submissions(db_path: Path, resume_id: str) -> int:
    """Delete all submissions for a given resume ID. Returns number of rows deleted."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "DELETE FROM submissions WHERE resume_id = ?", (resume_id,)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted


def reset_db(db_path: Path) -> None:
    """Delete all submissions (works for both lecture 2 and 3)."""
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM submissions")
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Lecture 3 helpers (same schema as lecture 2 — reuse the same functions)
# ---------------------------------------------------------------------------

# Lecture 3 uses the same table schema as lecture 2: (team_name, resume_id) keying.
# The only difference is the DB file path and which CSV provides valid IDs.
# Reuse init_db, add_submission, get_all_submissions, delete_submission,
# delete_team_submissions, and reset_db with LECTURE3_DB_PATH.
