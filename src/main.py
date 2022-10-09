from unittest import result
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import asyncio
from pydantic import BaseModel
from typing import Optional, List
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
questions_dict = questions_db.to_dict(orient="records")


@api.get("/")
async def get_index():
    return {"grettings": "Welcome!"}


@api.get("/use")
async def get_use():
    try:
        questions_db = pd.DataFrame(jsonable_encoder(questions_dict))
        use_dict = (
            questions_db[["use", "subject"]]
            .groupby(["use", "subject"])
            .nunique()
            .reset_index()
            .to_dict(orient="records")
        )
        return use_dict
    except IndexError:
        return {}


@api.get("/questions")
async def get_questions():
    try:
        return questions_dict
    except IndexError:
        return {}


@api.get("/exam/{use}/subject/{subject}/nb/{nb}")
async def get_exam(use: str, subject: str, nb: int):
    try:
        subject_lst = list(subject.split(","))
        questions_db = pd.DataFrame(jsonable_encoder(questions_dict))
        questions_lst = questions_db[
            (questions_db["use"] == use) & (questions_db["subject"].isin(subject_lst))
        ]
        if nb > len(questions_lst):
            nb = len(questions_lst)
        exam_dict = questions_lst.sample(n=nb).to_dict(orient="records")
        return exam_dict
    except IndexError:
        return {}


class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None
    remark: Optional[str] = None


@api.post("/question")
async def put_question(question: Question):
    try:
        questions_dict.append(question)
        return questions_dict
    except IndexError:
        return {}
