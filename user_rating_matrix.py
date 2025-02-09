import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

items = pd.read_csv('ml-latest-small/movies.csv', delimiter=',', names=['movieId', 'title', 'genres'])
ratings = pd.read_csv('ml-latest-small/ratings.csv', delimiter=',', names=["userId","movieId","rating","timestamp"])

# convertendo algumas séries em numérico por estarem em str
ratings['rating'] = pd.to_numeric(ratings['rating'], errors="coerce")
ratings['userId'] = pd.to_numeric(ratings['userId'], errors="coerce")
ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors="coerce")

items['movieId'] = pd.to_numeric(items['movieId'], errors="coerce")

def generate_rating_matrix(ratings: pd.DataFrame) -> pd.DataFrame:

    user_movie_matrix = ratings.pivot_table(index="userId", columns="movieId", values="rating").fillna(0)

    return user_movie_matrix


user_rating_matrix = generate_rating_matrix(ratings=ratings)
# print(user_rating_matrix)
