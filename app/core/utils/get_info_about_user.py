from aiogram.types import Message

from typing import Tuple, Optional
from dataclasses import dataclass

from app.core import logger


@dataclass
class UserInfo:
    id: Optional[int]
    username: str
    first_name: str
    last_name: Optional[str]


async def get_user_info(message: Message) -> UserInfo:
    user_id = getattr(message.from_user, "id", None)
    username = getattr(message.from_user, "username", "User")
    first_name = getattr(message.from_user, "first_name", username)
    last_name = getattr(message.from_user, "last_name", None)
    
    user_info = UserInfo(
        id = user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    
    logger.info(f"Info about {user_info.username} (ID: {user_info.id}) collected.")
    return user_info