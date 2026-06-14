import json
import os
import torch
import time

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

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

print("Loading model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

with open(
    "job_description.txt",
    "r",
    encoding="utf-8"
) as f:

    jd_text = f.read()

candidates = []

with open(
    "candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:
        candidates.append(json.loads(line))

print("Candidates Loaded:", len(candidates))

def candidate_text(c):

    text = ""

    p = c["profile"]

    text += p["headline"] + " "
    text += p["summary"] + " "
    text += p["current_title"] + " "

    for job in c["career_history"]:
        text += job["title"] + " "
        text += job["description"] + " "

    for skill in c["skills"]:
        text += skill["name"] + " "

    return text


print("Preparing texts...")

texts = [
    candidate_text(c)
    for c in candidates
]

EMBEDDING_FILE = "candidate_embeddings.pt"

if os.path.exists(EMBEDDING_FILE):

    print("Loading saved embeddings...")

    candidate_embeddings = torch.load(
        EMBEDDING_FILE,
        weights_only=False
    )

else:

    print("Creating candidate embeddings...")

    start = time.time()

    candidate_embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        convert_to_tensor=True
    )

    torch.save(
        candidate_embeddings,
        EMBEDDING_FILE
    )

    end = time.time()

    print(
        "Embedding Time:",
        end - start,
        "seconds"
    )

    print(
        "Embeddings saved to",
        EMBEDDING_FILE
    )

print("Creating JD embedding...")

jd_embedding = model.encode(
    jd_text,
    convert_to_tensor=True
)

results = []

print("Scoring candidates...")

for i, c in enumerate(candidates):

    semantic_similarity = float(
        cos_sim(
            jd_embedding,
            candidate_embeddings[i]
        )
    )

    score = (
    0.25 * semantic_similarity
    + 0.15 * experience_score(c)
    + 0.20 * title_score(c)
    + 0.15 * behavioral_score(c)
    + 0.15 * retrieval_score(c)
    + 0.05 * company_score(c)
    + 0.10 * activity_score(c)
    + 0.03 * location_score(c)
    + 0.05 * stability_score(c)
    - 0.20 * negative_title_penalty(c)
    )

    results.append(
        (
            c["candidate_id"],
            c["profile"]["current_title"],
            score
        )
    )

results.sort(
    key=lambda x: x[2],
    reverse=True
)

with open(
    "final_ranking_results.csv",
    "w",
    encoding="utf-8"
) as f:

    f.write("candidate_id,title,score\n")

    for r in results:

        f.write(
            f"{r[0]},{r[1]},{r[2]}\n"
        )

print("\nTOP 50\n")

for r in results[:50]:
    print(r)