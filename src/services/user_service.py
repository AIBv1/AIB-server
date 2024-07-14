import logging

from src.database.model import User, SNSType
from src.services.mysql_service import MySqlService


class UserService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mysql_service = MySqlService()


    async def get_or_create_user(self, email: str, sns_type: str, username: str, profile_image_url: str):
        user = await self.mysql_service.get_user_by_email_and_type(email, sns_type)
        if user:
            return user
        else:
            user = User(username= username, email=email, sns_type=SNSType.KAKAO, profile_image_url=profile_image_url)
            return await self.mysql_service.insert_user(user)
