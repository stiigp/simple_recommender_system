import pandas as pd
from items_ratings_treated import items, ratings

# this does generate the rating matrix, where users are the rows, movies are the columns and the value of
# the cell mat[i][j] is the rating user i gave to film j.
# will use on the rest of the project

def generate_rating_matrix(ratings: pd.DataFrame) -> pd.DataFrame:

    user_movie_matrix = ratings.pivot_table(index="userId", columns="movieId", values="rating").fillna(0)

    return user_movie_matrix


rating_matrix = generate_rating_matrix(ratings=ratings)

if __name__ == "__main__":
    print(rating_matrix)
