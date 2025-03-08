# generates IMDB weighted ratings for the ~9700 movies of the database

import pandas as pd

# THESE WORK FOR THE 1998 100K DATASET
# items = pd.read_csv('ml-100k/u.item', encoding="latin-1", delimiter="|", names=["movie id", "movie title", "release date", "video release date",
#               "IMDb URL", "unknown", "Action", "Adventure", "Animation",
#               "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
#               "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
#               "Thriller", "War", "Western"])
# ratings = pd.read_csv('ml-100k/u.data', encoding="utf-8", delimiter="\t", names=["userId", "movieId", "rating", "timestamp"])

items = pd.read_csv('../ml-latest-small/movies.csv', delimiter=',', names=['movieId', 'title', 'genres'])
ratings = pd.read_csv('../ml-latest-small/ratings.csv', delimiter=',', names=["userId", "movieId", "rating", "timestamp"])

# convertendo algumas séries em numérico por estarem em str
ratings['rating'] = pd.to_numeric(ratings['rating'], errors="coerce")
ratings['userId'] = pd.to_numeric(ratings['userId'], errors="coerce")
ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors="coerce")

items['movieId'] = pd.to_numeric(items['movieId'], errors="coerce")


def general_average(dataset: pd.DataFrame) -> float:
    return dataset['rating'].mean()

# v
def ratings_number(dataset: pd.DataFrame, item_id: int) -> int:
    return dataset[dataset['movieId'] == item_id].shape[0]

# R
def movie_avg_rating(dataset: pd.DataFrame, item_id: int) -> float:

    movie_ratings = dataset[dataset['movieId'] == item_id]['rating']

    return movie_ratings.mean() if not movie_ratings.empty else 0

# final imdb rating standard calculus
def imdb_rating(dataset: pd.DataFrame, item_id: int, m: int, c: float) -> float:
    # WR = v / (v + m) * R + m / (v + m) * C

    # R = média de avaliações do filme
    # v = número de avaliações do filme
    # m = número mínimo de avaliações considerado relevante (exemplo: 100)
    # C = média geral das avaliações de todos os filmes

    r = movie_avg_rating(dataset, item_id)
    v = ratings_number(dataset, item_id)

    return v / (v + m) * r + m / (v + m) * c if v + m != 0 else c

def imdb_rating_penalizing_age(dataset: pd.DataFrame, item_id: int, m: int, c: float, year: int, tax: float=0.98, current_year: int=2025) -> float:
    # WR = v / (v + m) * R + m / (v + m) * C

    # R = média de avaliações do filme
    # v = número de avaliações do filme
    # m = número mínimo de avaliações considerado relevante (exemplo: 100)
    # C = média geral das avaliações de todos os filmes

    r = movie_avg_rating(dataset, item_id)
    v = ratings_number(dataset, item_id)

    penalty = tax ** (current_year - year)

    return (v / (v + m) * r + m / (v + m) * c) * penalty if v + m != 0 else c

# print(general_average(ratings)) # must be around 3.5

# print(ratings_number(ratings, 945)) # must be 3; can be checked by searching for "944" on the 'u.data' file

# print(movie_avg_rating(ratings, 945)) # 4.0

# print(imdb_rating(ratings, 945, 100, general_average(ratings))) # around 3.51

imdb_rating_list = []

c = general_average(ratings)

def filtering_based_on_number_ratings(items: pd.DataFrame, ratings: pd.DataFrame, n: int) -> pd.DataFrame:
    df_merged = items.merge(ratings, on="movieId", how="inner")
    df_filtered = df_merged.groupby("title").filter(lambda x: len(x) > n)

    # made these just to check if my filtering was going all right
    # df_count_ratings = df_filtered.groupby("title")["rating"].count().reset_index()
    # print(df_count_ratings)

    return df_filtered

items = filtering_based_on_number_ratings(items=items, ratings=ratings, n=10)
items = items.drop_duplicates(subset=["movieId", "title"])

for index, row in items[1:].iterrows():

    try:
        year = int(row['title'][-5:-1])
    except:
        year = 0

    wr = imdb_rating_penalizing_age(ratings, row['movieId'], 100, c, year=year, tax=0.995) # tax=0.995 equivale a 0.5% de taxa por ano, que ficou relativamente equilibrado
    imdb_rating_list.append({"title": row["title"], "imdb_rating": wr, "year": year})
    


# so this list is the top rated movies considering a rating system that uses weights and also penalizes older movies
# for balance. it was also filtered not to consider movies that have less than
imdb_rating_list.sort(key=lambda x: x['imdb_rating'], reverse=True)

# I consider this implementation of imdb/weighted rating a failure, it favors old movies way too much, I would have to directly filter films by age.
# it is a possibility to implement penalties based on the age of the film or favor newer films, but it is rather simpler to just get the best rated
# movies with the medium of ratings implementing a minimum of ratings to avoid outliers with very few ratings, which I'm working on right now

for item in imdb_rating_list[:10]:
    print(f"Movie: {item['title']}\tRating: {item['imdb_rating']}\tYear: {item['year']}")
