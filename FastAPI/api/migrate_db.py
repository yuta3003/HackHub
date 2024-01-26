"""
Database Initialization Module.

This module provides functionality for initializing the database using SQLAlchemy.
It includes a function `reset_database` to drop and recreate all tables defined in the models.

Usage:
    - When executed as the main script, it resets the database.

Note:
    Make sure to update the `DB_URL` variable with the appropriate database connection URL.

Example:
    python migrate_db.py
"""
from sqlalchemy import create_engine

from api.models.model import Base

DB_URL = "mysql+pymysql://root@db:3306/prod?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    """
    Reset the database by dropping and recreating all tables.

    This function uses the SQLAlchemy Base.metadata object to drop and create tables
    defined in the models.

    Usage:
        Call this function to reset the database.

    Example:
        reset_database()
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
