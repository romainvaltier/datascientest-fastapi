from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import pandas as pd

description = """
Datascientest-fastapi API helps you do awesome stuff. 🚀

## User

You will be able to:
* Get current **user**.

## Use

You will be able to:
* Get a list of **use** and associated **subject(s)**.

## Questions

You will be able to:
* Get a list of all **questions**

## Question

You will be able to:
* Add one **question** to existing set of questions.

## Exam

Ypu will be able to:

* Generate a random set of questions for an **exam** with specific use and a list of associated subject(s).
"""

api = FastAPI(title="Datascientest-fastapi exam", description=description)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# user database
# users_db = {"alice": "wonderland", "bob": "builder", "clementine": "mandarine"}
users = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("wonderland"),
    },
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("builder"),
    },
    "clementine": {
        "username": "clementine",
        "hashed_password": pwd_context.hash("mandarine"),
    },
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("4dm1N"),
    },
}


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not (users.get(username)) or not (
        pwd_context.verify(credentials.password, users[username]["hashed_password"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


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
    return {"message": "Welcome to {} !".format(api.title)}


@api.get("/user")
async def current_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)


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
async def get_questions(username: str = Depends(get_current_user)):
    if username != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only an administrator can list all questions",
            headers={"WWW-Authenticate": "Basic"},
        )
    return questions_dict


class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: Optional[str] = None
    responseB: Optional[str] = None
    responseC: Optional[str] = None
    responseD: Optional[str] = None
    remark: Optional[str] = None


@api.post("/question")
async def put_question(question: Question):
    try:
        questions_dict.append(jsonable_encoder(question))
        return question
    except IndexError:
        return {}


@api.get("/exam")
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
