import pandas as pd
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from treating_data.items_ratings_treated import items, ratings
from typing import List, Dict

SEARCHLY_URL = os.getenv("SEARCHLY_URL")

class LoadingIntoES:
    def __init__(self):
        self.es = Elasticsearch(SEARCHLY_URL)
        self.movies_index_name = "movies_index"
        self.ratings_index_name = "ratings_index"
        self.items_list = items.to_dict(orient="records")
        self.ratings_list = ratings.to_dict(orient="records")

    def create_movies_index(self):
        movies_mapping = {
            "properties": {
                "movieId": {
                    "type": "integer"
                },
                "title": {
                    "type": "text"
                },
                "genres": {
                    "type": "text"
                },
                "timestamp": {
                    "type": "text"
                }
            }
        }

        self.es.indices.create(index=self.movies_index_name, body={"mappings": movies_mapping}, headers={"Content-Type": "application/json"})

    def delete_movies_index(self):
        self.es.indices.delete(index=self.movies_index_name)

    def dump_movies_on_index(self):
        actions = [{"_index": self.movies_index_name, "_source": {"title": f"movie_{movie['movieId']}", "body": movie}, "_id": f"movie_{movie['movieId']}"} for movie in self.items_list]

        bulk(self.es, actions)

    # aparentemente não funciona, consertar depois :)
    def delete_all_movies(self):
        for i in range(len(self.items_list)):
            try:
                self.es.delete(index=self.movies_index_name, id=f'movie_{i}')
            except:
                pass

    def select_movie(self, movie_id: int) -> Dict:
        doc = self.es.get(index=self.movies_index_name, id=f"movie_{movie_id}")

        return doc.body['_source']['body']

    def create_ratings_index(self):
        ratings_mapping = {
            "properties": {
                "userId": {
                    "type": "integer"
                },
                "movieId": {
                    "type": "integer"
                },
                "rating": {
                    "type": "integer"
                },
                "timestamp": {
                    "type": "text"
                }
            }
        }

        self.es.indices.create(index=self.ratings_index_name, body={"mappings": ratings_mapping})

    def delete_ratings_index(self):
        self.es.indices.delete(index=self.ratings_index_name)

    def dump_ratings_on_index(self):
        # print(self.ratings_list[0])
        actions = [{"_index": self.ratings_index_name, "_source": {"userId": rating["userId"], "movieId": rating['movieId'], "rating":rating['rating'], "timestamp": rating['timestamp']}} for rating in self.ratings_list]

        bulk(self.es, actions)

    def select_ratings(self, movie_id: int) -> List[Dict]:
        doc = self.es.search(index=self.ratings_index_name, body={"query": {"match": {"movieId": movie_id}}})['hits']['hits']
        res = [rating['_source'] for rating in doc]

        return res

loading_obj = LoadingIntoES()

# loading_obj.delete_movies_index()
# loading_obj.create_movies_index()
# loading_obj.dump_movies_on_index()
# movie = loading_obj.select_movie(movie_id=500)
# loading_obj.delete_all_movies()

# loading_obj.create_ratings_index()
# loading_obj.delete_ratings_index()
# loading_obj.dump_ratings_on_index()
# ratings_result = loading_obj.select_ratings(500)
# print(ratings_result)
