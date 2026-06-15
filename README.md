# Redrob Intelligent Candidate Discovery & Ranking Challenge

## Overview

This project implements an AI-assisted candidate ranking system for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

The goal is to rank candidates for a Senior AI Engineer role by combining semantic similarity, domain-specific signals, behavioral indicators, and recruiter-oriented heuristics rather than relying purely on keyword matching.

The ranking system attempts to capture the intent behind the job description, particularly the emphasis on:

* Retrieval and ranking systems
* Search and recommendation experience
* Production ML deployments
* Product-company experience
* Candidate availability and recruiter engagement
* Long-term fit rather than keyword density

---

## Methodology

The final candidate score is computed as a weighted combination of multiple signals:

### 1. Semantic Similarity

SentenceTransformer (`all-MiniLM-L6-v2`) embeddings are generated for:

* Full Job Description
* Candidate profile text

Cosine similarity between the candidate embedding and job description embedding provides the semantic relevance score.

Weight: **0.20**

---

### 2. Experience Score

Rewards candidates whose experience falls within the preferred range specified in the JD.

Preferred range:

* 5–9 years → highest score
* 4–10 years → partial score

Weight: **0.15**

---

### 3. Title Score

Rewards titles strongly aligned with the target role, including:

* AI Engineer
* Senior AI Engineer
* Machine Learning Engineer
* Search Engineer
* Recommendation Systems Engineer
* NLP Engineer
* Applied ML Engineer
* Lead AI Engineer
* Staff Machine Learning Engineer

Weight: **0.20**

---

### 4. Behavioral Score

Captures hiring readiness using Redrob platform signals:

* Open-to-work status
* Recruiter response rate
* Interview completion rate
* Notice period
* Relocation willingness
* GitHub activity
* Recruiter saves
* Search visibility
* Profile verification signals

Weight: **0.18**

---

### 5. Retrieval / Ranking Expertise

Detects evidence of:

* Search systems
* Retrieval systems
* Recommendation systems
* Learning-to-Rank
* Semantic Search
* Hybrid Retrieval
* NDCG / MRR / MAP evaluation

Weight: **0.15**

---

### 6. Company Background

Rewards experience at product-focused companies and lightly penalizes candidates whose experience is entirely consulting-oriented.

Weight: **0.05**

---

### 7. Activity Score

Measures current market activity:

* Applications submitted
* Recruiter saves
* Search appearances
* Profile views

Weight: **0.12**

---

### 8. Location Score

Rewards candidates located in:

* Pune
* Noida
* Delhi NCR
* Mumbai
* Hyderabad

Also considers relocation willingness.

Weight: **0.03**

---

### 9. Stability Score

Measures average tenure across previous jobs to identify candidates likely to remain with the company long-term.

Weight: **0.05**

---

### 10. Negative Title Penalty

Penalizes obviously unrelated profiles such as:

* Marketing Manager
* Sales Executive
* Graphic Designer
* Accountant
* Civil Engineer

Also applies a smaller penalty to junior-level profiles for this senior role.

Penalty Weight: **-0.20**

---

## Final Scoring Formula

Final Score =
(0.20 × Semantic Similarity)

* (0.15 × Experience Score)
* (0.20 × Title Score)
* (0.18 × Behavioral Score)
* (0.15 × Retrieval Score)
* (0.05 × Company Score)
* (0.12 × Activity Score)
* (0.03 × Location Score)
* (0.05 × Stability Score)
  − (0.20 × Negative Title Penalty)

---

## Precomputation

Candidate embeddings are generated using:

sentence-transformers/all-MiniLM-L6-v2

and cached locally as:

candidate_embeddings.pt

This significantly reduces repeated execution time during experimentation.

If the embedding cache is unavailable, embeddings are automatically regenerated.

---

## Repository Structure

main_batch.py - 
Primary ranking pipeline

ranker.py -
Feature engineering and scoring functions

top100.py -
Extracts Top-100 candidates

generate_submission.py -
Generates final submission.csv

job_description.txt -
Target job description

submission.csv -
Final submission file

---

## Reproducing Results

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Place Dataset Files

Ensure the following files are present in the project root:

* candidates.jsonl
* job_description.txt

### Step 4: Run the Complete Pipeline

```bash
python main_batch.py; python top100.py; python generate_submission.py
```

This pipeline performs:

1. Candidate ranking (`main_batch.py`)
2. Top-100 extraction (`top100.py`)
3. Submission file generation (`generate_submission.py`)

### Output

The final output file will be:

```text
submission.csv
```

### Notes

* Candidate embeddings are automatically cached as `candidate_embeddings.pt`.
* On the first run, embeddings are generated if the cache file is not present.
* On subsequent runs, cached embeddings are loaded automatically, significantly reducing runtime.
* No external APIs or network access are required during ranking.

## Live Demo

A Streamlit sandbox is provided for evaluation.

The demo allows reviewers to:

1. Upload a candidate sample (≤100 candidates)
2. Run the ranking pipeline end-to-end
3. View ranked candidates
4. Download the ranked CSV output

Sandbox URL:

[<Streamlit link>](https://vniharika33-intelligent-candidate-discovery-ranking--app-z4rbx3.streamlit.app/)

The sandbox uses the same scoring methodology as the full submission but is intended for small evaluation samples to satisfy the challenge compute constraints.


## Design Philosophy

The solution intentionally avoids pure keyword matching.

Instead, it attempts to model the intent behind the JD by prioritizing:

* Production ML experience
* Retrieval and ranking systems
* Product-company backgrounds
* Candidate availability
* Behavioral engagement signals

This approach is designed to better surface candidates who are genuinely relevant to the role rather than candidates who simply contain matching keywords.

---



## Author

Vennamaneni Niharika -
Redrob Intelligent Candidate Discovery & Ranking Challenge Submission
