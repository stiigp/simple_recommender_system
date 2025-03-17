import pandas as pd
import os

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from utils.crypt import hash_senha, verifica_senha
from elasticsearch import Elasticsearch
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from recommendations.pearson_correlation_recommendations import build_pearson_similarity_matrix
from recommendations.cosine_similarity_recommendations import build_cosine_similarity_matrix
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from Classes.Usuario import Usuario
from Classes.UsuarioModel import UsuarioModel

if os.getenv("RAILWAY_ENVIRONMENT") is None:
    load_dotenv()

SEARCHLY_URL = os.getenv("SEARCHLY_URL")
MOVIES_INDEX_NAME = os.getenv("MOVIES_INDEX_NAME")
API_KEY = os.getenv("API_KEY")
HEADER_NAME = os.getenv("HEADER_NAME")
MYSQL_URL = os.getenv("MYSQL_URL")

engine = create_engine(MYSQL_URL, pool_recycle=280, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

api_key_header = APIKeyHeader(name=HEADER_NAME, auto_error=False)

app = FastAPI()
es = Elasticsearch(SEARCHLY_URL)

@app.get("/")
async def root():
    return {"message": "eita porra dum caralho agora fudeu de vez"}

async def auth(key: str=Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail=f"Chave inválida: {key} vs {API_KEY}")

@app.get("/movies_list/{start}/{movies_number}", dependencies=[Depends(auth)])
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

@app.get('/movies/{movieId}', dependencies=[Depends(auth)])
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


@app.get('/similar_movies_pearson/{movieId}', dependencies=[Depends(auth)])
async def getSimilarMoviesPearson(movieId: int):
    rating_matrix = pd.read_parquet("treating_data/rating_matrix.parquet")

    pearson_similarity_matrix = build_pearson_similarity_matrix(rating_matrix)

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


@app.get('/similar_movies_cosine/{movieId}', dependencies=[Depends(auth)])
async def getSimilarMoviesCosine(movieId: int):
    rating_matrix = pd.read_parquet("treating_data/rating_matrix.parquet")

    cosine_similarity_matrix = build_cosine_similarity_matrix(rating_matrix)

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

@app.post('/register_user', dependencies=[Depends(auth)])
async def registrarUsuario(usuario: UsuarioModel):
    db = SessionLocal()

    senha_hasheada = hash_senha(usuario.password)

    try:
        db = SessionLocal()

        novoUsuario = Usuario(
            username=usuario.username,
            email=usuario.email,
            senha=senha_hasheada
        )

        db.add(novoUsuario)
        db.commit()
        db.refresh(novoUsuario)

        return {
            "message": "User criado com sucesso!",
            "User": {
                "userId": novoUsuario.id,
                "userName": novoUsuario.username,
                "userEmail": novoUsuario.email
            }
        }

    except SQLAlchemyError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {e}"
        )
    finally:
        db.close()


