import pandas as pd

df = pd.read_csv("final_ranking_results.csv")

top100 = df.head(100)

top100.to_csv(
    "top100.csv",
    index=False
)

print("Top 100 saved.")