from fastapi import FastAPI
import requests
from config import SEARCHLY_URL
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch(SEARCHLY_URL)

MOVIES_INDEX_NAME = "movies_index"

@app.get("/")
async def root():
    return {"message": "eita porra dum caralho agora fudeu de vez"}


@app.get("/movies_list/{start}/{movies_number}")
async def getMovies(start:int=0, movies_number:int=10):

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
async def getMovieById(movieId:int):
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
