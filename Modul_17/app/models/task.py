from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db import Base
from app.backend.db_depends import get_db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy import insert, select, update, delete
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, Session
from app.models import *
from typing import Annotated
from app.routers.schemas import CreateUser, UpdateUser
from slugify import slugify

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    slug = Column(String, unique=True, index=True)
    user = relationship('User', back_populates='tasks')



router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks():
    pass

@router.get("/task_id")
async def task_by_id():
    pass

@router.post("/create")
async def create_task():
    pass

@router.put("/update")
async def update_task():
    pass

@router.delete("/delete")
async def delete_task():
    pass

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
