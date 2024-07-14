import logging
from typing import Optional

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import MySQLClient
from src.database.model import User, SNSType
from sqlalchemy.future import select



class MySqlService:
    def __init__(self, query_limit=1000):
        self.mysql_client = MySQLClient()
        self.query_limit = query_limit
        self.logger = logging.getLogger(__name__)


    async def get_user_by_email_and_type(self, email: str, sns_type: str, db: AsyncSession = Depends(MySQLClient.get_db)) -> Optional[User]:
        async for session in self.mysql_client.get_db():
            result = await session.execute(
                select(User).filter_by(email=email, sns_type=sns_type)
            )
            return result.scalars().first()

    async def insert_user(self, user: User):
        async for session in self.mysql_client.get_db():
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
