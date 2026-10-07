# Leaderboard

A multi-lecture leaderboard system for the AI Development course. Each leaderboard tracks student team submissions for a different assignment, with real-time scoring grids and admin controls.

## Lectures

### Lecture 2 — Resume Scoring
Students build their first LLM-powered resume scoring system. Teams submit numeric scores (0–100) for a set of real anonymized resumes, and the leaderboard displays a grid of teams vs. resume IDs. This assignment introduces prompt engineering fundamentals: students iterate on system prompts to produce consistent, calibrated scores.

### Lecture 3 — Context Engineering (Gold/Silver Discrimination)
Building on Lecture 2, students must now discriminate between "gold" (strong-fit) and "silver" (weak-fit) resumes. The leaderboard color-codes resume IDs by tier and computes per-team metrics: gold/silver mean gap, rank separation, and cost. This assignment teaches context engineering — crafting prompts and few-shot examples that produce meaningfully different outputs for different input categories.

## Screenshots

| Home | Lecture 2 | Lecture 3 |
|------|-----------|-----------|
| ![Home](./screenshots/home.png) | ![L2](./screenshots/lecture2.png) | ![L3](./screenshots/lecture3.png) |

## Running

```bash
# Start the server
uvicorn leaderboard.app:app --reload

# Run tests
python -m leaderboard.test_leaderboards

# Capture screenshots (seeds test data, launches Playwright)
python -m leaderboard.screenshot_leaderboards
```
