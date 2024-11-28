from sqlalchemy.orm import Session
from fastapi import Depends
from app.backend.db import Sessionlocal


async def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()