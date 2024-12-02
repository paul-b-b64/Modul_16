from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import relationship, Session
from app.models import *
from typing import Annotated
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix="/task", tags=["task"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/")
async def all_tasks(db: DbSession):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/task_id")
async def task_by_id(db: DbSession, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    return task


@router.post("/create")
async def create_task(db: DbSession, create_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=user_id))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
async def update_task(db: DbSession, update_task: UpdateTask, id: int):
    task_updated = db.scalar(select(Task).where(Task.id == id))
    if task_updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')

    db.execute(update(Task).where(Task.id == id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }


@router.delete("/delete")
async def delete_task(db: DbSession, id: int):
    task_deleted = db.scalar(select(Task).where(Task.id == id))
    if task_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')

    db.execute(delete(Task).where(Task.id == id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task deleted successful!'
    }
