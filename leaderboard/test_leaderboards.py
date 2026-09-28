"""Test scripts for lecture 2, lecture 3, and lecture 4 leaderboards."""

import random
from fastapi.testclient import TestClient
from leaderboard.app import app

API_KEY = "leaderboard-api-key"
HEADERS = {"X-API-Key": API_KEY}


def test_lecture2():
    print("=" * 60)
    print("LECTURE 2 LEADERBOARD TESTS")
    print("=" * 60)

    with TestClient(app) as client:
        # Health check
        r = client.get("/lecture2/api/health")
        assert r.status_code == 200
        print(f"  [PASS] Health check: {r.json()}")

        # Reset
        r = client.post("/lecture2/api/reset", headers=HEADERS)
        assert r.status_code == 200
        print(f"  [PASS] Reset: {r.json()}")

        # Submit scores for 2 teams, 3 resumes each
        teams = ["Team Alpha", "Team Beta"]
        resume_ids = ["10089434", "10247517", "10265057"]
        for team in teams:
            for rid in resume_ids:
                score = round(random.uniform(30, 95), 1)
                r = client.post(
                    "/lecture2/api/submit",
                    json={"team_name": team, "resume_id": rid, "score": score},
                    headers=HEADERS,
                )
                assert r.status_code == 200
        print(f"  [PASS] Submitted {len(teams) * len(resume_ids)} scores")

        # Get submissions
        r = client.get("/lecture2/api/submissions")
        assert r.status_code == 200
        subs = r.json()
        assert len(subs) == 6
        print(f"  [PASS] Get submissions: {len(subs)} rows")

        # Update a score (INSERT OR REPLACE)
        r = client.post(
            "/lecture2/api/submit",
            json={"team_name": "Team Alpha", "resume_id": "10089434", "score": 99.0},
            headers=HEADERS,
        )
        assert r.status_code == 200
        r = client.get("/lecture2/api/submissions")
        updated = [s for s in r.json() if s["team_name"] == "Team Alpha" and s["resume_id"] == "10089434"]
        assert updated[0]["score"] == 99.0
        print(f"  [PASS] Score update (INSERT OR REPLACE): score={updated[0]['score']}")

        # Invalid resume ID
        r = client.post(
            "/lecture2/api/submit",
            json={"team_name": "Team Alpha", "resume_id": "INVALID", "score": 50},
            headers=HEADERS,
        )
        assert r.status_code == 400
        print(f"  [PASS] Invalid resume_id rejected: {r.json()['detail']}")

        # Score out of range
        r = client.post(
            "/lecture2/api/submit",
            json={"team_name": "Team Alpha", "resume_id": "10089434", "score": 150},
            headers=HEADERS,
        )
        assert r.status_code == 400
        print(f"  [PASS] Out-of-range score rejected: {r.json()['detail']}")

        # Bad API key
        r = client.post(
            "/lecture2/api/submit",
            json={"team_name": "Team Alpha", "resume_id": "10089434", "score": 50},
            headers={"X-API-Key": "wrong-key"},
        )
        assert r.status_code == 401
        print(f"  [PASS] Bad API key rejected: {r.json()['detail']}")

        # Delete single submission
        r = client.request(
            "DELETE",
            "/lecture2/api/submit",
            json={"team_name": "Team Alpha", "resume_id": "10089434"},
            headers=HEADERS,
        )
        assert r.status_code == 200
        print(f"  [PASS] Delete single submission: {r.json()}")

        # Delete team
        r = client.post(
            "/lecture2/api/delete_team",
            json={"team_name": "Team Beta"},
            headers=HEADERS,
        )
        assert r.status_code == 200
        assert r.json()["deleted"] == 3
        print(f"  [PASS] Delete team: {r.json()}")

        # HTML page renders
        r = client.get("/lecture2")
        assert r.status_code == 200
        assert "Leaderboard" in r.text
        print(f"  [PASS] HTML page renders ({len(r.text)} chars)")

        # Seed
        r = client.post("/lecture2/api/seed", headers=HEADERS)
        assert r.status_code == 200
        print(f"  [PASS] Seed: {r.json()}")

        # Cleanup
        r = client.post("/lecture2/api/reset", headers=HEADERS)
        print(f"  [PASS] Final reset")

    print("  ALL LECTURE 2 TESTS PASSED\n")


def test_lecture3():
    print("=" * 60)
    print("LECTURE 3 LEADERBOARD TESTS")
    print("=" * 60)

    with TestClient(app) as client:
        # Health check
        r = client.get("/lecture3/api/health")
        assert r.status_code == 200
        print(f"  [PASS] Health check: {r.json()}")

        # Reset
        r = client.post("/lecture3/api/reset", headers=HEADERS)
        assert r.status_code == 200
        print(f"  [PASS] Reset: {r.json()}")

        # Submit gold scores (should be high)
        gold_scores = {"g01": 88, "g02": 92}
        for rid, score in gold_scores.items():
            r = client.post(
                "/lecture3/api/submit",
                json={"team_name": "TestTeam", "resume_id": rid, "score": score},
                headers=HEADERS,
            )
            assert r.status_code == 200
        print(f"  [PASS] Submitted {len(gold_scores)} gold scores")

        # Submit silver scores (should be low)
        silver_scores = {"s01": 15, "s02": 22}
        for rid, score in silver_scores.items():
            r = client.post(
                "/lecture3/api/submit",
                json={"team_name": "TestTeam", "resume_id": rid, "score": score},
                headers=HEADERS,
            )
            assert r.status_code == 200
        print(f"  [PASS] Submitted {len(silver_scores)} silver scores")

        # Submit some wild scores
        wild_scores = {"10089434": 45, "10247517": 60}
        for rid, score in wild_scores.items():
            r = client.post(
                "/lecture3/api/submit",
                json={"team_name": "TestTeam", "resume_id": rid, "score": score},
                headers=HEADERS,
            )
            assert r.status_code == 200
        print(f"  [PASS] Submitted {len(wild_scores)} wild scores")

        # Get submissions
        r = client.get("/lecture3/api/submissions")
        assert r.status_code == 200
        subs = r.json()
        assert len(subs) == 6
        print(f"  [PASS] Get submissions: {len(subs)} rows")

        # Get metrics for TestTeam
        r = client.get("/lecture3/api/metrics?team=TestTeam")
        assert r.status_code == 200
        metrics = r.json()
        assert len(metrics) == 1
        m = metrics[0]
        print(f"  [PASS] Metrics for TestTeam:")
        print(f"         gold_mean={m['gold_mean']}, silver_mean={m['silver_mean']}")
        print(f"         gold_silver_gap={m['gold_silver_gap']}")
        print(f"         rank_separation={m['rank_separation']}")
        print(f"         gold_std={m['gold_std']}, silver_std={m['silver_std']}")
        print(f"         num_gold={m['num_gold']}, num_silver={m['num_silver']}, num_wild={m['num_wild']}")

        # Validate metrics
        assert m["gold_mean"] > m["silver_mean"], "Gold mean should exceed silver mean"
        assert m["gold_silver_gap"] > 0, "Gold-silver gap should be positive"
        assert m["rank_separation"] == 1.0, "Perfect separation expected with these scores"
        assert m["num_gold"] == 2
        assert m["num_silver"] == 2
        assert m["num_wild"] == 2
        print(f"  [PASS] Metrics validation passed")

        # Get all metrics (no filter)
        r = client.get("/lecture3/api/metrics")
        assert r.status_code == 200
        all_metrics = r.json()
        assert len(all_metrics) >= 1
        print(f"  [PASS] All metrics: {len(all_metrics)} team(s)")

        # Submit for a second team
        r = client.post(
            "/lecture3/api/submit",
            json={"team_name": "Team2", "resume_id": "g01", "score": 50},
            headers=HEADERS,
        )
        assert r.status_code == 200
        r = client.post(
            "/lecture3/api/submit",
            json={"team_name": "Team2", "resume_id": "s01", "score": 55},
            headers=HEADERS,
        )
        assert r.status_code == 200
        r = client.get("/lecture3/api/metrics?team=Team2")
        m2 = r.json()[0]
        assert m2["gold_silver_gap"] < 0, "Team2 has bad separation (silver > gold)"
        assert m2["rank_separation"] == 0.0
        print(f"  [PASS] Team2 bad separation: gap={m2['gold_silver_gap']}, rank_sep={m2['rank_separation']}")

        # Invalid resume ID
        r = client.post(
            "/lecture3/api/submit",
            json={"team_name": "TestTeam", "resume_id": "INVALID", "score": 50},
            headers=HEADERS,
        )
        assert r.status_code == 400
        print(f"  [PASS] Invalid resume_id rejected")

        # Delete single submission
        r = client.request(
            "DELETE",
            "/lecture3/api/submit",
            json={"team_name": "TestTeam", "resume_id": "g01"},
            headers=HEADERS,
        )
        assert r.status_code == 200
        print(f"  [PASS] Delete single submission: {r.json()}")

        # Delete team
        r = client.post(
            "/lecture3/api/delete_team",
            json={"team_name": "Team2"},
            headers=HEADERS,
        )
        assert r.status_code == 200
        assert r.json()["deleted"] == 2
        print(f"  [PASS] Delete team: {r.json()}")

        # HTML page renders with grid
        r = client.get("/lecture3")
        assert r.status_code == 200
        assert "Leaderboard" in r.text
        assert "Resume ID" in r.text
        print(f"  [PASS] HTML page renders ({len(r.text)} chars)")

        # Root shows lecture picker
        r = client.get("/")
        assert r.status_code == 200
        assert "/lecture2" in r.text
        assert "/lecture3" in r.text
        print(f"  [PASS] Root shows lecture picker page")

        # Cleanup
        r = client.post("/lecture3/api/reset", headers=HEADERS)
        print(f"  [PASS] Final reset")

    print("  ALL LECTURE 3 TESTS PASSED\n")


def test_lecture4():
    print("=" * 60)
    print("LECTURE 4 LEADERBOARD TESTS")
    print("=" * 60)

    with TestClient(app) as client:
        # Health check
        r = client.get("/lecture4/api/health")
        assert r.status_code == 200
        print(f"  [PASS] Health check: {r.json()}")

        # Reset
        r = client.post("/lecture4/api/reset", headers=HEADERS)
        assert r.status_code == 200
        print(f"  [PASS] Reset: {r.json()}")

        # Submit outcomes for 2 teams, 3 resumes each
        teams = ["Team Alpha", "Team Beta"]
        resume_ids = ["g01", "g02", "s01"]
        outcomes = ["INTERVIEW", "REJECT", "REVIEW"]
        for team in teams:
            for i, rid in enumerate(resume_ids):
                outcome = outcomes[i % len(outcomes)]
                r = client.post(
                    "/lecture4/api/submit",
                    json={
                        "team_name": team,
                        "resume_id": rid,
                        "outcome": outcome,
                        "email_text": f"Test email for {rid} from {team}",
                        "score": round(random.uniform(30, 95), 1),
                        "cost": round(random.uniform(0.001, 0.01), 5),
                    },
                    headers=HEADERS,
                )
                assert r.status_code == 200
        print(f"  [PASS] Submitted {len(teams) * len(resume_ids)} outcomes")

        # Get submissions
        r = client.get("/lecture4/api/submissions")
        assert r.status_code == 200
        subs = r.json()
        assert len(subs) == 6
        print(f"  [PASS] Get submissions: {len(subs)} rows")

        # Update a submission (INSERT OR REPLACE)
        r = client.post(
            "/lecture4/api/submit",
            json={
                "team_name": "Team Alpha",
                "resume_id": "g01",
                "outcome": "REJECT",
                "email_text": "Updated rejection email",
                "score": 42.0,
            },
            headers=HEADERS,
        )
        assert r.status_code == 200
        r = client.get("/lecture4/api/submissions")
        updated = [s for s in r.json() if s["team_name"] == "Team Alpha" and s["resume_id"] == "g01"]
        assert updated[0]["outcome"] == "REJECT"
        print(f"  [PASS] Submission update (INSERT OR REPLACE): outcome={updated[0]['outcome']}")

        # Invalid resume ID
        r = client.post(
            "/lecture4/api/submit",
            json={
                "team_name": "Team Alpha",
                "resume_id": "INVALID",
                "outcome": "INTERVIEW",
                "email_text": "test",
            },
            headers=HEADERS,
        )
        assert r.status_code == 400
        print(f"  [PASS] Invalid resume_id rejected: {r.json()['detail']}")

        # Invalid outcome
        r = client.post(
            "/lecture4/api/submit",
            json={
                "team_name": "Team Alpha",
                "resume_id": "g01",
                "outcome": "INVALID",
                "email_text": "test",
            },
            headers=HEADERS,
        )
        assert r.status_code == 400
        print(f"  [PASS] Invalid outcome rejected: {r.json()['detail']}")

        # Bad API key
        r = client.post(
            "/lecture4/api/submit",
            json={
                "team_name": "Team Alpha",
                "resume_id": "g01",
                "outcome": "INTERVIEW",
                "email_text": "test",
            },
            headers={"X-API-Key": "wrong-key"},
        )
        assert r.status_code == 401
        print(f"  [PASS] Bad API key rejected: {r.json()['detail']}")

        # Delete single submission
        r = client.request(
            "DELETE",
            "/lecture4/api/submit",
            json={"team_name": "Team Alpha", "resume_id": "g01"},
            headers=HEADERS,
        )
        assert r.status_code == 200
        print(f"  [PASS] Delete single submission: {r.json()}")

        # Delete team
        r = client.post(
            "/lecture4/api/delete_team",
            json={"team_name": "Team Beta"},
            headers=HEADERS,
        )
        assert r.status_code == 200
        assert r.json()["deleted"] == 3
        print(f"  [PASS] Delete team: {r.json()}")

        # HTML page renders
        r = client.get("/lecture4")
        assert r.status_code == 200
        assert "Leaderboard" in r.text
        print(f"  [PASS] HTML page renders ({len(r.text)} chars)")

        # Seed
        r = client.post("/lecture4/api/seed", headers=HEADERS)
        assert r.status_code == 200
        print(f"  [PASS] Seed: {r.json()}")

        # Cleanup
        r = client.post("/lecture4/api/reset", headers=HEADERS)
        print(f"  [PASS] Final reset")

    print("  ALL LECTURE 4 TESTS PASSED\n")


if __name__ == "__main__":
    test_lecture2()
    test_lecture3()
    test_lecture4()
    print("ALL TESTS PASSED")
