import pandas as pd
from user_rating_matrix import generate_rating_matrix
from best_average_ratings import filtering_based_on_number_ratings

items = pd.read_csv('ml-latest-small/movies.csv', delimiter=',', names=['movieId', 'title', 'genres'])
ratings = pd.read_csv('ml-latest-small/ratings.csv', delimiter=',', names=["userId","movieId","rating","timestamp"])

# convertendo algumas séries em numérico por estarem em str
ratings['rating'] = pd.to_numeric(ratings['rating'], errors="coerce")
ratings['userId'] = pd.to_numeric(ratings['userId'], errors="coerce")
ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors="coerce")

items['movieId'] = pd.to_numeric(items['movieId'], errors="coerce")

# -- REFAZER ESSE TREM, PRECISO DE UMA FUNCAO QUE FILTRE AS AVALIACOES E NAO SOMENTE OS FILMES
items_filtered = filtering_based_on_number_ratings(items=items, ratings=ratings, n=50)
# print(items_filtered)

def filtering_ratings_based_on_items(items: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
    # print(ratings[ratings['movieId'].isin(items["movieId"])])
    return ratings[ratings['movieId'].isin(items["movieId"])]

def _build_pearson_similarity_matrix(user_rating_matrix: pd.DataFrame) -> pd.DataFrame:

    similarity_between_movies = user_rating_matrix.corr(method='pearson')

    return similarity_between_movies

def generate_recommendation(user_rating_matrix: pd.DataFrame, movieId: int) -> pd.Series:
    pearson_similarity_matrix = _build_pearson_similarity_matrix(user_rating_matrix=user_rating_matrix)

    return pearson_similarity_matrix[movieId].sort_values(ascending=False).iloc[1:6]

ratings_filtered = filtering_ratings_based_on_items(items=items_filtered, ratings=ratings)

user_rating_matrix = generate_rating_matrix(ratings=ratings_filtered)

recommendations = generate_recommendation(user_rating_matrix=user_rating_matrix, movieId=58559)

print(f"Recommendations for the movie {items[items['movieId'] == 58559]['title'].iloc[0]}:")

for recommendation in recommendations.index:
    print(items[items['movieId'] == recommendation]['title'].iloc[0])

print("These recommendations were generated by Pearson Correlation Coefficient!")
