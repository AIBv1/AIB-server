import os
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class MySQLClient:
    def __init__(self):
        self.connection_url = self.get_connection_url()
        self.engine = create_async_engine(
            self.connection_url, echo=True
        )
        self.sessionLocal = sessionmaker(
            bind = self.engine, class_=AsyncSession, expired_on_commit=False
        )

    @staticmethod
    def get_connection_url():
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        return f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    async def get_db(self):
        async with AsyncSession(self.engine) as session:
            yield session

