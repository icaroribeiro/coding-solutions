import time
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import List, Optional

import uvicorn
from aiocache import cached
from database import User, get_async_db, initialize_database
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/hello")
def hello_func():
    return "Hello World 1"


class UserResponseSchema(BaseModel):
    id: Optional[int]
    name: Optional[str] = Field(default=None)
    email: str = Field(
        default=None,
        description="It's an optional field that is not necessary to return in the response body.",
    )


class UserSchema(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str] = None

    class Config:
        from_attributes = True


@cached(ttl=timedelta(hours=1).total_seconds())
# @cached(
#     ttl=timedelta(hours=1).total_seconds(),
#     key=lambda self, list1, int2, int3: (
#         tuple(list1) if isinstance(list1, list) else list1
#     ),
# )
async def get_users_from_server(db: AsyncSession, selected_fields: List[str]):
    print("Get users from server...")
    map_attrs = [getattr(User, f) for f in selected_fields]
    stmt = select(User).options(load_only(*map_attrs))
    result = await db.scalars(stmt)
    return result.all()


@app.get("/", response_model=List[UserResponseSchema], response_model_exclude_none=True)
async def get_users(
    db: AsyncSession = Depends(get_async_db),
) -> List[UserResponseSchema]:
    start_time = time.time()
    selected_fields = ["id", "name"]
    users_from_server = await get_users_from_server(db, selected_fields)
    end_time = time.time()
    print(f"With caching: Time = {end_time - start_time:.5f} seconds")
    users = [UserSchema.model_validate(user.__dict__) for user in users_from_server]
    users_to_respond = [
        UserResponseSchema.model_validate(
            {
                key: value
                for key, value in user.model_dump().items()
                if key in selected_fields
            }
        )
        for user in users
    ]
    return users_to_respond


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
    )
