from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd

api = FastAPI()

# user database
users_db = {"alice": "wonderland", "bob": "builder", "clementine": "mandarine"}

# questions database
questions_db = pd.read_csv(
    "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv",
    sep=",",
    header=0,
)


@api.get("/")
def get_index():
    return {"data": "hello world"}


@api.get("/users")
def get_users():
    try:
        return users_db
    except IndexError:
        return {}


@api.get("/questions")
def get_questions():
    try:
        return questions_db.to_json(orient="index", force_ascii=False)
    except IndexError:
        return {}


@api.get("/exam/{nb_of_quest:int}")
def get_exam(nb_of_quest):
    try:
        return questions_db.sample(n=nb_of_quest).to_json(
            orient="index", force_ascii=False
        )
    except IndexError:
        return {}
