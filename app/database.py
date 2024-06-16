import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine  # Synchronous create_engine for initial database creation
from databases import Database
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Create an asynchronous database connection
database = Database(DATABASE_URL)

# Create an asynchronous SQLAlchemy engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Asynchronous session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


# Synchronous function to ensure database creation
def initialize_database():
    sync_engine = create_engine(DATABASE_URL.replace("postgresql+asyncpg", "postgresql"), echo=True)
    if not database_exists(sync_engine.url):
        print("Creating database...")
        create_database(sync_engine.url)
    else:
        print("Database already exists.")


# Function to get the async database connection
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
