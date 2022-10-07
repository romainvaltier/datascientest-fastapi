from fastapi import FastAPI
import pandas as pd

api = FastAPI()

# user database
user_db = {"alice": "wonderland", "bob": "builder", "clementine": "mandarine"}

# questions database
questions_db = pd.read_csv(
    "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv",
    sep=",",
    header=0,
)


@api.get("/")
def get_index():
    return {"method": "get", "endpoint": "/"}


@api.get("/permissions")
def get_permissions():
    return {"method": "get", "endpoint": "/other"}
