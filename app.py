import pandas as pd
import streamlit as st

st.title("Redrob Candidate Ranking Demo")

uploaded_file = st.file_uploader(
    "Upload ranking results CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Top Candidates")

    st.dataframe(df.head(20))