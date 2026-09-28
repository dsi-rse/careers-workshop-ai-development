"""Seed the lecture 4 leaderboard via the API so it works against the deployed server."""

import random
import httpx

BASE_URL = "http://ai-leaderboard.site"
API_KEY = "leaderboard-api-key"

TEAMS = [
    "Alpha Dogs", "Bayesian Bandits", "Cache Money", "Data Dynamos",
    "Error 404", "Feature Creeps", "Gradient Gang", "Hallucination Station",
    "Inference Engine", "JSON Bourne", "Kernel Panic", "Lambda Lords",
    "Model Misfits", "Neural Ninjas", "Overfitters", "Prompt Pirates",
]

RESUME_IDS = ["g01", "g02", "s01", "s02",
              "10840430", "16899268", "24083609", "25990239"]

INTERVIEW_EMAILS = [
    "Thank you for your application for the Senior Full-Stack Engineer position. Your extensive experience with C#/.NET, React, and SQL Server stood out to our team. We were particularly impressed by your work on microservices architecture and your AWS deployment experience. We'd love to move forward with a technical interview — our team will reach out shortly to find a time that works for you.",
    "We've reviewed your application and are excited about what you could bring to our engineering team. Your strong background in .NET development combined with your frontend expertise in Angular is exactly what we're looking for. Your experience leading agile teams and mentoring junior developers is a great bonus. Let's schedule a technical assessment — expect to hear from our recruiting coordinator within the next few days.",
    "Your resume caught our attention immediately. With over 8 years of full-stack development and deep expertise in the .NET ecosystem, you're an excellent match for this role. We'd like to invite you to a technical interview where you can learn more about our team and we can explore how your skills align with our current projects. Our team will follow up with scheduling details.",
    "We appreciate you taking the time to apply for our Senior Full-Stack Engineer role. Your combination of C# backend skills and modern JavaScript framework experience is compelling, and your track record with CI/CD pipelines shows the kind of engineering maturity we value. We'd like to schedule a conversation with our hiring manager to discuss next steps.",
    "After reviewing your application, we're confident you'd be a strong addition to our team. Your hands-on experience with Entity Framework, SQL Server optimization, and React development checks all the boxes for this position. We especially liked seeing your contributions to open-source .NET projects. Let's set up a technical interview — you'll hear from us soon.",
]

REJECT_EMAILS = [
    "Thank you for your interest in the Senior Full-Stack Engineer position. After careful consideration, we've decided to move forward with candidates whose experience more closely aligns with our current technical stack, particularly in .NET/C# backend development. We encourage you to continue developing your skills and wish you the best in your job search.",
    "We appreciate you applying for this role. While your background shows promise, we're looking for candidates with more extensive experience in our core technologies (.NET, SQL Server, and modern JavaScript frameworks). We'd encourage you to explore our junior developer openings, which might be a better fit for your current experience level.",
    "Thank you for considering our team. After reviewing your application against our requirements for a Senior Full-Stack Engineer, we've determined that the role requires a different skill set than what your resume reflects. We value the experience you do have and encourage you to keep an eye on future openings that may be a better match.",
    "We wanted to let you know that we've completed our review of applications for the Senior Full-Stack Engineer position. Unfortunately, we won't be moving forward with your candidacy at this time. The role requires significant backend experience with C#/.NET, which we didn't find sufficient evidence of in your resume. We wish you all the best.",
    "Thank you for your application. We received many qualified candidates and after thorough evaluation, we've decided to proceed with applicants whose backgrounds more directly match our technical requirements. Your skills in other areas are impressive, and we encourage you to apply for roles where those strengths would be the primary focus.",
]

REVIEW_EMAILS = [
    "Thank you for applying to our Senior Full-Stack Engineer position. Your application has been flagged for additional review by our hiring committee. While you bring some relevant experience, we'd like our team leads to take a closer look at how your skills might fit within our specific technical environment. You should expect to hear back from us within the next week.",
    "We're currently reviewing your application in more detail. Your background presents an interesting mix of skills that our team would like to evaluate further. We want to make sure we give your application the attention it deserves, so our senior engineers will be reviewing it this week. We'll be in touch with next steps soon.",
    "Your application for the Senior Full-Stack Engineer role is under additional review. Your experience caught our attention, but we want to ensure the best fit for both you and our team. Our hiring panel will discuss your candidacy in our next review meeting. We appreciate your patience and will follow up shortly.",
    "We wanted to update you on the status of your application. Your resume is being reviewed by our technical leads, as your background raises some interesting questions about how your skills could translate to our stack. We'll have a decision for you within the next few business days. Thank you for your patience.",
]

random.seed(42)

# First reset the leaderboard
print("Resetting lecture 4 leaderboard...")
resp = httpx.post(f"{BASE_URL}/lecture4/api/reset", headers={"X-API-Key": API_KEY})
print(f"  Reset: {resp.status_code} {resp.json()}")

count = 0
errors = 0

with httpx.Client(timeout=30) as client:
    for team in TEAMS:
        # Each team submits for a random subset of resumes (60-90% coverage)
        num_resumes = random.randint(len(RESUME_IDS) * 6 // 10, len(RESUME_IDS))
        selected = random.sample(RESUME_IDS, num_resumes)

        for rid in selected:
            # Gold resumes → mostly INTERVIEW, silver → mostly REJECT, wild → mixed
            if rid.startswith('g'):
                outcome = random.choices(["INTERVIEW", "REVIEW", "REJECT"], weights=[75, 20, 5])[0]
                score = random.randint(78, 98)
            elif rid.startswith('s'):
                outcome = random.choices(["REJECT", "REVIEW", "INTERVIEW"], weights=[65, 25, 10])[0]
                score = random.randint(30, 72)
            else:
                outcome = random.choices(["REJECT", "REVIEW", "INTERVIEW"], weights=[50, 30, 20])[0]
                score = random.randint(5, 55)

            if outcome == "INTERVIEW":
                email = random.choice(INTERVIEW_EMAILS)
            elif outcome == "REJECT":
                email = random.choice(REJECT_EMAILS)
            else:
                email = random.choice(REVIEW_EMAILS)

            # Add candidate reference
            email = f"Re: Application #{rid}\n\n{email}"

            cost = round(random.uniform(0.001, 0.015), 5)

            payload = {
                "team_name": team,
                "resume_id": rid,
                "outcome": outcome,
                "email_text": email,
                "score": score,
                "cost": cost,
            }

            resp = client.post(
                f"{BASE_URL}/lecture4/api/submit",
                json=payload,
                headers={"X-API-Key": API_KEY},
            )
            if resp.status_code == 200:
                count += 1
            else:
                errors += 1
                print(f"  ERROR {resp.status_code}: {resp.text} (team={team}, rid={rid})")

        print(f"  {team}: submitted {len(selected)} resumes")

print(f"\nDone. {count} submissions, {errors} errors across {len(TEAMS)} teams.")
