from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+asyncpg://pguser:pgsecret@localhost:5433/pgdb"

# Async engine for async queries
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

# Async session for async queries
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Create all tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


# Dependency to get async DB session
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


# Startup: Initialize the database
async def initialize_database():
    await init_db()
