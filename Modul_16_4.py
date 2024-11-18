from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users")
def get_users():
    return users


@app.post("/user/{username}/{age}")
def create_user(user: User, username: str, age: int):
    user.id = max([x.id for x in users], default=0) + 1
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, username: str, age: int):
    try:
        index = None
        for i in range(len(users)):
            if users[i].id == user_id:
                index = i
        edit_user = users[index]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except TypeError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    try:
        index = None
        for i in range(len(users)):
            if users[i].id == user_id:
                index = i
        popped_user = users.pop(index)
        return popped_user
    except TypeError:
        raise HTTPException(status_code=404, detail="User was not found")
