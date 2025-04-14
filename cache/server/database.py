from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

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

# Define metadata
metadata = MetaData()

# Define User Table
User = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


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
