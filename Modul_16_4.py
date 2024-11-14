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
    return f"User {user.username} registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str, username: str, age: int):

#     try:
#         edit_message = messages_db[message_id]
#         edit_message.text = message
#         return f"Message updated!"
#     except IndexError:
#         raise HTTPException(status_code=404, detail="Message not found")

#
# @app.delete("/user/{user_id}")
# async def delete_user(user_id: str) -> str:
#     users.pop(user_id)
#     return f"The user {user_id} has been deleted"
