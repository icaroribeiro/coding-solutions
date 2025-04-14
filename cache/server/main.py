from contextlib import asynccontextmanager
from datetime import datetime

import pytz
import uvicorn
from database import User, get_async_db, initialize_database
from fastapi import Depends, FastAPI, HTTPException
from server.pagination import create_pagination_response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/hello")
def hello_func():
    return "Hello World 1"


cache = dict()


async def get_user_from_server(
    user_id: int, db: AsyncSession, reference_date: datetime
):
    if reference_date not in cache:
        print("Fetching user from server...")
        result = await db.execute(select(User).where(User.c.id == user_id))
        user = result.fetchone()
        cache[reference_date] = user

    return cache[reference_date]


async def get_and_count_users_from_server(
    page: int,
    limit: int,
    reference_date: datetime,
    db: AsyncSession,
):
    _tuple = (pagination_config.page, pagination_config.limit, reference_date)
    if _tuple not in cache:
        print("Fetching users from server...")
        result = await db.execute(
            select(User).where(User.c.reference_date == reference_date)
        )
        users = result.fetchall()
        pagination_config.total_records = len(users)
        pagination_config.records = users
        cache[_tuple] = create_pagination_response()

    return cache[_tuple]


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    reference_date = datetime.now(tz=pytz.timezone("America/Sao_Paulo")).date()
    print(f"Getting user on {reference_date}...")
    user = await get_user_from_server(user_id, db, reference_date)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    reference_date = datetime.now(tz=pytz.timezone("America/Sao_Paulo")).date()
    print(f"Getting user on {reference_date}...")
    user = await get_users_from_server(db, reference_date)
    if not paginate:
        raise HTTPException(status_code=404, detail="Users not found")

    pagination_config.total_records = len(users)
    pagination_config.records = users
    return {"id": user.id, "name": user.name}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
    )
