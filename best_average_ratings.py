import pandas as pd

items = pd.read_csv('ml-latest-small/movies.csv', delimiter=',', names=['movieId', 'title', 'genres'])
ratings = pd.read_csv('ml-latest-small/ratings.csv', delimiter=',', names=["userId","movieId","rating","timestamp"])

# convertendo algumas séries em numérico por estarem em str
ratings['rating'] = pd.to_numeric(ratings['rating'], errors="coerce")
ratings['userId'] = pd.to_numeric(ratings['userId'], errors="coerce")
ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors="coerce")

items['movieId'] = pd.to_numeric(items['movieId'], errors="coerce")

def ratings_number(dataset: pd.DataFrame, item_id: int) -> int:
    return dataset[dataset['movieId'] == item_id].shape[0]

def movie_avg_rating(dataset: pd.DataFrame, item_id: int) -> float:

    movie_ratings = dataset[dataset['movieId'] == item_id]['rating']

    return movie_ratings.mean() if not movie_ratings.empty else 0

def filtering_based_on_number_ratings(items: pd.DataFrame, ratings: pd.DataFrame, n: int) -> pd.DataFrame:
    df_merged = items.merge(ratings, on="movieId", how="inner")

    # --- I swear this makes sense ---
    # groupby returns multiple dataframes, each one for a value of the selected column
    # so it filters it based on the lenght of each dataframe, which corresponds to the number of ratings,
    # which is what we want to filter based on
    df_filtered = df_merged.groupby("title").filter(lambda x: len(x) > n)

    # but df_filtered has all the ratings of the selected movies merged with its name and id
    # so we eliminate the duplicates with this
    df_unique = df_filtered.drop_duplicates(subset=["movieId", "title"]).drop(columns=['userId', "rating"])

    # made these just to check if my filtering was going all right
    # df_count_ratings = df_filtered.groupby("title")["rating"].count().reset_index()
    # print(df_count_ratings)

    return df_unique

def rank_by_mean(items: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
    df_merged = items.merge(ratings, how="inner", on="movieId")[1:]
    # print(df_merged.columns)

    df_grouped = df_merged.groupby("title")["rating"].mean().reset_index().sort_values(by="rating", ascending=False).reset_index()

    return df_grouped

df_filtered = filtering_based_on_number_ratings(items=items, ratings=ratings, n=75)
grouped_by_mean = rank_by_mean(items=df_filtered, ratings=ratings)

# print(grouped_by_mean[:10])
