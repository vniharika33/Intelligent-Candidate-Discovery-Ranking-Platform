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

    skills = [
        s["name"]
        for s in c["skills"]
    ]

    retrieval_skills = []

    for skill in [
        "Information Retrieval",
        "Learning to Rank",
        "Semantic Search",
        "Vector Search",
        "Recommendation Systems",
        "BM25",
        "FAISS",
        "Pinecone",
        "Qdrant",
        "Weaviate",
        "Milvus",
        "OpenSearch",
        "Elasticsearch"
    ]:

        if skill in skills:
            retrieval_skills.append(skill)

    reason = f"{title} with {exp:.1f} yrs experience"

    if retrieval_skills:

        reason += (
            "; retrieval/ranking expertise ("
            + ", ".join(retrieval_skills[:3])
            + ")"
        )

    if company_score(c) > 0:
        reason += "; product-company background"

    if behavioral_score(c) >= 0.6:
        reason += "; strong recruiter/activity signals"

    if (
        not c["redrob_signals"]["open_to_work_flag"]
        and c["redrob_signals"]["recruiter_response_rate"] < 0.2
    ):
        reason += "; lower availability signals"

    return reason + "."

with open(
    "submission.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow(
        [
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    )

    for rank, row in enumerate(
        top100,
        start=1
    ):

        cid = row["candidate_id"]

        reason = generate_reasoning(
            candidates[cid]
        )

        writer.writerow(
            [
                cid,
                rank,
                row["score"],
                reason
            ]
        )

print("submission.csv created")