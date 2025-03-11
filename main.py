import pandas as pd
import os
from fastapi import FastAPI
import requests
from elasticsearch import Elasticsearch
from typing import List
from recommendations.pearson_correlation_recommendations import _build_pearson_similarity_matrix
from recommendations.cosine_similarity_recommendations import _build_cosine_similarity_matrix
from dotenv import load_dotenv

if os.getenv("RAILWAY_ENVIRONMENT") is None:
    from dotenv import load_dotenv
    load_dotenv()

SEARCHLY_URL = os.getenv("SEARCHLY_URL")
MOVIES_INDEX_NAME = os.getenv("MOVIES_INDEX_NAME")

app = FastAPI()
es = Elasticsearch(SEARCHLY_URL)

@app.get("/")
async def root():
    return {"message": "eita porra dum caralho agora fudeu de vez"}


@app.get("/movies_list/{start}/{movies_number}")
async def getMovies(start:int=0, movies_number:int=10) -> List:

    req_body = {
        "query": {
            "match_all": {}
        },
        "size": movies_number,
        "from": start
    }

    response = es.search(index=MOVIES_INDEX_NAME, body=req_body)

    return [film['_source'] for film in response['hits']['hits']]

@app.get('/movies/{movieId}')
async def getMovieById(movieId:int) -> List:
    body = {
        'query': {
            "term": {
                "body.movieId": {
                    "value": movieId
                }
            }
        }
    }

    response = es.search(index=MOVIES_INDEX_NAME, body=body)

    return response['hits']['hits']


@app.get('/similar_movies_pearson/{movieId}')
async def getSimilarMoviesPearson(movieId: int):
    rating_matrix = pd.read_parquet("treating_data/rating_matrix.parquet")

    pearson_similarity_matrix = _build_pearson_similarity_matrix(rating_matrix)

    recommendations_index = pearson_similarity_matrix[movieId].sort_values(ascending=False).iloc[1:6].index

    result = []

    for rec_id in recommendations_index:

        body = {
            "query": {
                "term": {
                    "body.movieId": rec_id
                }
            }
        }

        response = es.search(index=MOVIES_INDEX_NAME, body=body)

        result.append(response['hits']['hits'][0]['_source']['body']['title'])

    return result


@app.get('/similar_movies_cosine/{movieId}')
async def getSimilarMoviesCosine(movieId: int):
    rating_matrix = pd.read_parquet("treating_data/rating_matrix.parquet")

    cosine_similarity_matrix = _build_cosine_similarity_matrix(rating_matrix)

    recommendations_index = cosine_similarity_matrix[movieId].sort_values(ascending=False).iloc[1:6].index

    result = []

    for rec_id in recommendations_index:
        body = {
            "query": {
                "term": {
                    "body.movieId": rec_id
                }
            }
        }

        response = es.search(index=MOVIES_INDEX_NAME, body=body)

        result.append(response['hits']['hits'][0]['_source']['body']['title'])

    return result


