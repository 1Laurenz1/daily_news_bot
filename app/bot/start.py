from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.core import logger, get_user_info
from app.database import user_repo, AsyncSessionLocal


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user_info = await get_user_info(message)
    user_id, username = user_info.id, user_info.username
    
    await message.answer(
        f"Hi, {username}! I'm your personal tech news curator!\n\n"
        "What I can do:\n"
        "- Gather news from Reddit, Hacker News, Habr\n"
        "- Filter by your interests using AI\n"
        "- Send a digest every morning\n\n"
        "Let's set up your interests!\n"
        "Write the technologies you're interested in, separated by commas:\n\n"
        "Example: Python, Machine Learning, Web Development, DevOps"
    )
    logger.info(f"User {username}({user_id}) started the bot.")
    
    async with AsyncSessionLocal() as session:
        await user_repo.create_user(
            session,
            user_id,
            username
        )