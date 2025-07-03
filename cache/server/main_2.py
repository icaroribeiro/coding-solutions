import math
import time
from datetime import datetime, timedelta
from typing import List, Optional

import uvicorn
from cachetools import TTLCache, cached
from database_2 import User, get_db, initialize_database
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

app = FastAPI()


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


@cached(
    cache=TTLCache(
        maxsize=math.inf,
        ttl=timedelta(hours=1).total_seconds(),
        timer=lambda: datetime.now(),
    )
)
# @cached(
#     cache=TTLCache(
#         maxsize=math.inf,
#         ttl=timedelta(hours=1).total_seconds(),
#         timer=lambda: datetime.now(),
#     ),
#     key=lambda self, list1, int2, int3: (
#         tuple(list1) if isinstance(list1, list) else list1
#     ),
# )
def get_users_from_server(db: Session, selected_fields: List[str]):
    print("Get users from server 2...")
    map_attrs = [getattr(User, f) for f in selected_fields]
    stmt = select(User).options(load_only(*map_attrs))
    result = db.scalars(stmt)
    return result.all()


@app.get("/", response_model=List[UserResponseSchema], response_model_exclude_none=True)
def get_users(
    db: Session = Depends(get_db),
) -> List[UserResponseSchema]:
    start_time = time.time()
    selected_fields = ["id", "name"]
    users_from_server = get_users_from_server(db, selected_fields)
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
    initialize_database()
    uvicorn.run(
        app="main_2:app",
        host="0.0.0.0",
        port=8080,
    )
