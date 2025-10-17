from app.core import logger
from app.database import AsyncSessionLocal, User
from sqlalchemy import select

from aiogram import Bot


class NotificationService:
    def __init__(self):
        pass
    
    async def send_daily_news_for_user(self, user_id: int, bot: Bot) -> None:
        """Send a daily digest to a single user.
        The actual fetching/filtering of news is not implemented here.
        """
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User).where(User.user_id == user_id))
                user = result.scalar_one_or_none()

            if not user:
                logger.warning(f"User {user_id} not found; skipping digest send")
                return

            # Placeholder: prepare digest message
            interests = user.interests or []
            digest_lines = [
                "Good morning! Here's your tech digest.",
                f"Interests: {', '.join(interests) if interests else 'not set'}",
                "This is a placeholder message."
            ]
            text = "\n".join(digest_lines)

            await bot.send_message(chat_id=user.user_id, text=text)
            logger.info(f"Sent daily digest to user {user.user_id}")
        except Exception as e:
            logger.error(f"Error while sending digest to {user_id}: {e}")
        
        

notif_serv = NotificationService()