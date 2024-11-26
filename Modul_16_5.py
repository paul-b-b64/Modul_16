from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")


# users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


users: List[User] = [
    User(id=1, username="UrbanUser", age=24),
    User(id=2, username="UrbanTest", age=22),
    User(id=3, username="Capybara", age=60)
]


@app.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request):
    return templates.TemplateResponse('users.html', {"request": request, "users": users})


@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: int):
    try:
        index = None
        for i in range(len(users)):
            if users[i].id == user_id:
                index = i
        return templates.TemplateResponse("users.html", {"request": request, "users": users[index]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


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
