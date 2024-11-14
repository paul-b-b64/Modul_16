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
async def get_message() -> list:
    return users


@app.post("/user/{username}/{age}")
async def create_user(user: User, username: str, age: int):
    user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    try:
        popped_user = users.pop(user_id - 1)
        return popped_user
    except:
        raise HTTPException(status_code=404, detail="User was not found")
