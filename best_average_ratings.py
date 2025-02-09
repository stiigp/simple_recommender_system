import pandas as pd
from items_ratings_treated import items, ratings

def rank_by_mean(items: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
    df_merged = items.merge(ratings, how="inner", on="movieId")[1:]
    # print(df_merged.columns)

    df_grouped = df_merged.groupby("title")["rating"].mean().reset_index().sort_values(by="rating", ascending=False).reset_index()

    return df_grouped

if __name__ == "__main__":
    grouped_by_mean = rank_by_mean(items=items, ratings=ratings)
    print(grouped_by_mean[:10])
