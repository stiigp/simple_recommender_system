import os
import pandas as pd

from elasticsearch import Elasticsearch
from pandas import RangeIndex

SEARCHLY_URL = os.getenv("SEARCHLY_URL")
RATINGS_INDEX_NAME = os.getenv("RATINGS_INDEX_NAME")

# this does generate the rating matrix, where users are the rows, movies are the columns and the value of
# the cell mat[i][j] is the rating user i gave to film j.
# will use on the rest of the project

es = Elasticsearch(SEARCHLY_URL)

# this procedure should be executed periodically to update the rating matrix
# as it will save it in a relational format to be reused without generating it every time
def generate_rating_matrix() -> pd.DataFrame:
    body = {
        "query": {
            "match_all": {}
        },
        "size": 10000,
        'sort': [
            {"movieId": "asc"}
        ]
    }

    res = es.search(index=RATINGS_INDEX_NAME, body=body)
    docs = [doc['_source'] for doc in res['hits']['hits']]

    while len(res['hits']['hits']) > 0:
        body['search_after'] = res['hits']['hits'][-1]['sort']
        res = es.search(index=RATINGS_INDEX_NAME, body=body)
        print(len(res['hits']['hits']))
        docs += [doc['_source'] for doc in res['hits']['hits']]

    ratings = pd.DataFrame(docs)

    print(ratings)

    user_movie_matrix = ratings.pivot_table(index="userId", columns="movieId", values="rating").fillna(0)

    return user_movie_matrix

if __name__ == "__main__":

    rating_matrix = generate_rating_matrix()
    rating_matrix.to_parquet("rating_matrix.parquet")

    # print(rating_matrix)
