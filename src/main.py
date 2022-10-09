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
    return {"grettings": "welcome"}


@api.get("/users")
def get_users():
    try:
        return users_db
    except IndexError:
        return {}


@api.get("/use")
def get_use():
    try:
        return (
            questions_db[["use", "subject"]]
            .groupby(["use", "subject"])
            .nunique()
            .reset_index()
            .to_dict(orient="records")
        )
    except IndexError:
        return {}


@api.get("/questions")
def get_questions():
    try:
        return questions_db.to_json(orient="records", force_ascii=False)
    except IndexError:
        return {}


@api.get("/exam/{use}/subject/{subject}/nb/{nb:int}")
def get_exam(use, subject, nb):
    try:
        subject_lst = list(subject.split(","))
        questions_lst = questions_db[
            (questions_db["use"] == use) & (questions_db["subject"].isin(subject_lst))
        ]
        if nb > len(questions_lst):
            nb = len(questions_lst)
        return (
            questions_lst.sample(n=nb)
            .reset_index()
            .to_json(orient="records", force_ascii=False)
        )
    except IndexError:
        return {}
