"""Seed all three leaderboards with test data and capture full-page screenshots."""

import contextlib
import threading
import time

import uvicorn
from playwright.sync_api import sync_playwright

from leaderboard.app import app

PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"


def _run_server():
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")


def main():
    # Start the server in a background thread
    server_thread = threading.Thread(target=_run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # wait for server to start

    import httpx

    headers = {"X-API-Key": "leaderboard-api-key"}

    # Reset and seed all leaderboards
    with httpx.Client(base_url=BASE, timeout=30) as client:
        for lecture in ["lecture2", "lecture3", "lecture4"]:
            r = client.post(f"/{lecture}/api/reset", headers=headers)
            print(f"  Reset {lecture}: {r.status_code}")
            r = client.post(f"/{lecture}/api/seed", headers=headers)
            print(f"  Seed {lecture}: {r.status_code} {r.json()}")

    # Take screenshots with Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        pages = [
            ("/", "home"),
            ("/lecture2", "lecture2"),
            ("/lecture3", "lecture3"),
            ("/lecture4", "lecture4"),
        ]

        for path, name in pages:
            page.goto(f"{BASE}{path}")
            page.wait_for_load_state("networkidle")
            out = f"leaderboard/screenshots/{name}.png"
            page.screenshot(path=out, full_page=True)
            print(f"  Screenshot saved: {out}")

        browser.close()

    print("\nDone. Screenshots in leaderboard/screenshots/")


if __name__ == "__main__":
    main()
