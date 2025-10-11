from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.core import logger


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    username = message.from_user.username or "Uknown"
    user_id = getattr(message.from_user, "id", None)
    
    await message.answer(f"Hello, {username}!")
    logger.info(f"User {username}({user_id}) started the bot.")