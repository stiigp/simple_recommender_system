from fastapi import FastAPI
import requests
from config import SEARCHLY_URL

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "eita porra dum caralho agora fudeu de vez"}

@app.get("/movies/")
async def getMovies(start:int=0, movies_number:int=10):
    url = SEARCHLY_URL + f"/movies_index/_search?pretty=true&q=*:*&from={start}&size={movies_number}"
    response = requests.get(url=url)
    return response.json()
