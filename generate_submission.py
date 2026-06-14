import csv
import json

from ranker import (
    experience_score,
    title_score,
    behavioral_score,
    retrieval_score,
    negative_title_penalty,
    company_score,
    activity_score,
    location_score,
    stability_score
)

top100 = []

with open(
    "top100.csv",
    "r",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:
        top100.append(row)

print("Top100 Loaded:", len(top100))

candidates = {}

with open(
    "candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        c = json.loads(line)

        candidates[
            c["candidate_id"]
        ] = c

print(
    "Candidates Loaded:",
    len(candidates)
)

def generate_reasoning(c):

    title = c["profile"]["current_title"]

    exp = c["profile"]["years_of_experience"]

    reason_parts = []

    reason_parts.append(
        f"{title}; {exp:.1f} yrs experience"
    )

    if retrieval_score(c) >= 0.7:
        reason_parts.append(
            "strong retrieval/ranking background"
        )

    if company_score(c) > 0:
        reason_parts.append(
            "product-company experience"
        )

    if behavioral_score(c) >= 0.6:
        reason_parts.append(
            "high behavioral engagement"
        )

    if activity_score(c) >= 0.6:
        reason_parts.append(
            "active candidate"
        )

    return "; ".join(reason_parts) + "."

first_id = top100[0]["candidate_id"]

print(
    generate_reasoning(
        candidates[first_id]
    )
)