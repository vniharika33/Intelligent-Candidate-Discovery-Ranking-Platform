import json

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from ranker import experience_score
from ranker import title_score
from ranker import behavioral_score
from ranker import negative_title_penalty
from ranker import retrieval_score

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
        candidates.append(
            json.loads(line)
        )

def candidate_text(c):

    text = ""

    p = c["profile"]

    text += p["headline"] + " "
    text += p["current_title"] + " "

    for job in c["career_history"]:
        text += job["title"] + " "
        text += job["description"] + " "

    for skill in c["skills"]:
        text += skill["name"] + " "

    return text

print("Creating JD embedding...")

jd_focus = """
Senior AI Engineer

Production experience with embeddings-based retrieval systems

Vector databases:
Pinecone
Weaviate
Qdrant
Milvus
FAISS

Hybrid search

Ranking systems

Recommendation systems

Search systems

Matching systems

Python

NDCG
MRR
MAP

Evaluation frameworks

Product company experience

Production deployment

5-9 years experience
"""

jd_embedding = model.encode(
    jd_focus,
    convert_to_tensor=True
)

results = []

for c in candidates:

    txt = candidate_text(c)

    emb = model.encode(
        txt,
        convert_to_tensor=True
    )

    semantic_similarity = float(
    cos_sim(
        jd_embedding,
        emb
    )
    )

    score = (
      0.30 * semantic_similarity
      + 0.25 * experience_score(c)
      + 0.15 * title_score(c)
      + 0.10 * behavioral_score(c)
      + 0.20 * retrieval_score(c)
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

print("\nTOP 10\n")

for r in results[:50]:
    print(r)




