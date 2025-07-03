from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://pguser:pgsecret@localhost:5433/pgdb"

# Create a synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session maker for synchronous queries
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Create all tables
def init_db():
    metadata.create_all(engine)


# Dependency to get a synchronous DB session
def get_db():
    with SessionLocal() as session:
        yield session


def initialize_database():
    init_db()
