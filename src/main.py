from fastapi import FastAPI
import pandas as pd

api = FastAPI()

# user database
users_db = {"alice": "wonderland", "bob": "builder", "clementine": "mandarine"}

# questions database
df = pd.read_csv(
    "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv",
    sep=",",
    header=0,
)
questions_db = df.values.tolist()


@api.get("/")
def get_index():
    return {"data": "hello world"}


# previous code is not included
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    userid: Optional[int]
    name: str
    subscription: str


@api.put("/users")
def put_users(user: User):
    new_id = max(users_db, key=lambda u: u.get("user_id"))["user_id"]
    new_user = {
        "user_id": new_id + 1,
        "name": user.name,
        "subscription": user.subscription,
    }
    users_db.append(new_user)
    return new_user


@api.post("/users/{userid:int}")
def post_users(user: User, userid):
    try:
        old_user = list(filter(lambda x: x.get("user_id") == userid, users_db))[0]

        users_db.remove(old_user)

        old_user["name"] = user.name
        old_user["subscription"] = user.subscription

        users_db.append(old_user)
        return old_user

    except IndexError:
        return {}


@api.delete("/users/{userid:int}")
def delete_users(userid):
    try:
        old_user = list(filter(lambda x: x.get("user_id") == userid, users_db))[0]

        users_db.remove(old_user)
        return {"userid": userid, "deleted": True}
    except IndexError:
        return {}
