from fastapi import FastAPI
import asyncio
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
questions_db.fillna("", inplace=True)


@api.get("/")
async def get_index():
    return {"grettings": "Welcome!"}


@api.get("/users")
async def get_users():
    try:
        return users_db
    except IndexError:
        return {}


@api.get("/use")
async def get_use():
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
async def get_questions():
    try:
        return questions_db.to_dict(orient="records")
    except IndexError:
        return {}


@api.get("/exam/{use:str}/subject/{subject:str}/nb/{nb:int}")
async def get_exam(use, subject, nb):
    try:
        subject_lst = list(subject.split(","))
        questions_lst = questions_db[
            (questions_db["use"] == use) & (questions_db["subject"].isin(subject_lst))
        ]
        if nb > len(questions_lst):
            nb = len(questions_lst)
        return questions_lst.sample(n=nb).to_dict(orient="records")
    except IndexError:
        return {}
