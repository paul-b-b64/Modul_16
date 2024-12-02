from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import relationship, Session
from app.models import *
from typing import Annotated
from app.schemas import CreateUser, UpdateUser

router = APIRouter(prefix="/user", tags=["user"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/")
async def all_users(db: DbSession):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(db: DbSession, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    return user


@router.get("/user_id/tasks")
async def tasks_by_user_id(db: DbSession, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    tasks = db.scalar(select(Task).where(Task.user_id == user_id))
    if not tasks:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tasks was not found')
    return tasks


@router.post("/create")
async def create_user(db: DbSession, create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
async def update_user(db: DbSession, update_user: UpdateUser, user_id: int):
    user_updated = db.scalar(select(User).where(User.id == user_id))
    if user_updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete("/delete") # не удаляются задачи пользователя
async def delete_user(db: DbSession, user_id: int):
    user_deleted = db.scalar(select(User).where(User.id == user_id))
    if user_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    # tasks_of_user_deleted = db.scalars(select(Task).where(Task.user_id == user_id))
    # if tasks_of_user_deleted is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tasks was not found')
    # db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted successful!'
    }

