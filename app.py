import json
import pandas as pd
import streamlit as st

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

st.set_page_config(
    page_title="Redrob Candidate Ranker",
    layout="wide"
)

st.title("Redrob Candidate Ranking Demo")


uploaded_file = st.file_uploader(
    "Upload candidates.jsonl",
    type=["jsonl"]
)

if uploaded_file is not None:

    candidates = []

    for line in uploaded_file:

        candidates.append(
            json.loads(
                line.decode("utf-8")
            )
        )

    st.success(
        f"Loaded {len(candidates)} candidates"
    )

    if len(candidates) > 100:

        st.error(
            "Please upload at most 100 candidates."
        )

        st.stop()

    if st.button("Run Ranking"):

        with st.spinner("Loading model..."):

            model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

        with open(
            "job_description.txt",
            "r",
            encoding="utf-8"
        ) as f:

            jd_text = f.read()

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

        with st.spinner("Generating embeddings..."):

            texts = [
                candidate_text(c)
                for c in candidates
            ]

            candidate_embeddings = model.encode(
                texts,
                convert_to_tensor=True
            )

            jd_embedding = model.encode(
                jd_text,
                convert_to_tensor=True
            )

        with st.spinner("Scoring candidates..."):

            results = []

            for i, c in enumerate(candidates):

                semantic_similarity = float(
                    cos_sim(
                        jd_embedding,
                        candidate_embeddings[i]
                    )
                )

                score = (
                    0.20 * semantic_similarity
                    + 0.15 * experience_score(c)
                    + 0.20 * title_score(c)
                    + 0.18 * behavioral_score(c)
                    + 0.15 * retrieval_score(c)
                    + 0.05 * company_score(c)
                    + 0.12 * activity_score(c)
                    + 0.03 * location_score(c)
                    + 0.05 * stability_score(c)
                    - 0.20 * negative_title_penalty(c)
                )

                results.append(
                    {
                        "candidate_id":
                            c["candidate_id"],
                        "title":
                            c["profile"][
                                "current_title"
                            ],
                        "score":
                            round(score, 6)
                    }
                )

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="score",
            ascending=False
        )

        df = df.reset_index(
            drop=True
        )

        st.success(
            "Ranking completed successfully!"
        )

        st.subheader(
            "Ranked Candidates"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Ranked CSV",
            data=csv,
            file_name="ranked_candidates.csv",
            mime="text/csv"
        )