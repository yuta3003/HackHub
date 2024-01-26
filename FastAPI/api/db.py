"""
Asynchronous Database Module.

This module provides functionality for working with an asynchronous database
using SQLAlchemy's async capabilities.
It includes an asynchronous engine, session creation, and a function
to get an asynchronous database session.

Usage:
    - Import the 'async_engine', 'async_session', and 'Base' objects.
    - Use the 'get_db' coroutine function to obtain an asynchronous database session.

Example:
    async with get_db() as session:
        # Perform database operations using the 'session' object

Note:
    Make sure to update the 'ASYNC_DB_URL' variable
    with the appropriate asynchronous database connection URL.

"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/prod?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    """
    Coroutine function to get an asynchronous database session.

    Usage:
        Use 'async with get_db() as session:' to obtain an asynchronous database session.
        Perform database operations using the 'session' object within the asynchronous context.

    Example:
        async with get_db() as session:
            # Perform database operations using the 'session' object
    """
    async with async_session() as session:
        yield session
