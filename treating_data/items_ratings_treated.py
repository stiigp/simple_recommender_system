import pandas as pd
import os

base_path = os.path.dirname(__file__)

# --- MAJORLY IMPORTANT FILE FOR THE REST OF THE PROJECT ---
# this file gets the csv files from the dataset, converts some series from string to numeric
# and filters both tables based on the number of ratings, so that we don't consider films that have less than N ratings,
# some other pre-treatment of the data may be added later.
# the final "items" and "ratings" objects are the ones used by the rest of the program, so that I don't have to apply
# pre-treatment on every single python file
# ----------------------------------------------------------

def ratings_number(dataset: pd.DataFrame, item_id: int) -> int:
    return dataset[dataset['movieId'] == item_id].shape[0]

# this function filters the ITEMS but doesn't filter the ratings, will deal with it in the function below
def filtering_based_on_number_ratings(items: pd.DataFrame, ratings: pd.DataFrame, n: int) -> pd.DataFrame:
    df_merged = items.merge(ratings, on="movieId", how="inner").dropna()

    # --- I swear this makes sense ---
    # groupby returns multiple dataframes, each one for a value of the selected column
    # so it filters it based on the length of each dataframe, which corresponds to the number of ratings,
    # which is what we want to filter based on
    df_filtered = df_merged.groupby("title").filter(lambda x: len(x) > n)

    # but df_filtered has all the ratings of the selected movies merged with its name and id
    # so we eliminate the duplicates with this
    df_unique = df_filtered.drop_duplicates(subset=["movieId", "title"]).drop(columns=['userId', "rating"])

    # made these just to check if my filtering was going all right
    # df_count_ratings = df_filtered.groupby("title")["rating"].count().reset_index()
    # print(df_count_ratings)

    return df_unique

def filtering_ratings_based_on_items(items: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
    # print(ratings[ratings['movieId'].isin(items["movieId"])])
    return ratings[ratings['movieId'].isin(items["movieId"])]

items_path = os.path.join(base_path, "../ml-latest-small/movies.csv")
ratings_path = os.path.join(base_path, "../ml-latest-small/ratings.csv")

items = pd.read_csv(items_path, delimiter=',', names=['movieId', 'title', 'genres'])
ratings = pd.read_csv(ratings_path, delimiter=',', names=["userId", "movieId", "rating", "timestamp"])

# convertendo algumas séries em numérico por estarem em str
ratings['rating'] = pd.to_numeric(ratings['rating'], errors="coerce")
ratings['userId'] = pd.to_numeric(ratings['userId'], errors="coerce")
ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors="coerce")

items['movieId'] = pd.to_numeric(items['movieId'], errors="coerce")

# essas são as variáveis finais utilizadas pelo resto do projeto
items = filtering_based_on_number_ratings(items=items, ratings=ratings, n=10)
ratings = filtering_ratings_based_on_items(items=items, ratings=ratings)

# por padrão o .to_numeric seta pra um ponto flutuante, quero converter os valores para int
ratings['rating'] = ratings['rating'].astype(int)
ratings['userId'] = ratings['userId'].astype(int)
ratings['movieId'] = ratings['movieId'].astype(int)

items['movieId'] = items['movieId'].astype(int)
