from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext 

from app.core import logger, get_user_info
from app.database import user_repo, AsyncSessionLocal
from app.bot import InterestsState, NotificationTimeState
from app.scheduler.setup import reschedule_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    user_info = await get_user_info(message)
    user_id, username = user_info.id, user_info.username
    
    logger.info(f"User {username}({user_id}) started the bot.")
        
    async with AsyncSessionLocal() as session:
        user, is_new = await user_repo.create_user(
            session,
            user_id,
            username
        )
        
        if not user:
            logger.warning("⚠️Database error. User if not found.")
            await message.answer("⚠️ Database error. Please try again later.")
            return
        
        if not is_new:
            await message.answer(f"👏Welcome back, {username}!")
            return
    
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
        
    await state.set_state(InterestsState.interests)
    
    
@router.message(InterestsState.interests)
async def process_interests(message: Message, state: FSMContext) -> None:
    user_info = await get_user_info(message)
    user_id, username = user_info.id, user_info.username

    user_interests = [i.strip() for i in message.text.split(",") if i.strip()]
    
    await state.update_data(interests=user_interests)
    
    async with AsyncSessionLocal() as session:
        await user_repo.save_user_interests(
            session,
            user_id,
            username,
            user_interests
        )
    
    await message.answer(
        "✅Got it!\nYour interests:\n" + ", ".join(user_interests )
    )
    
    await state.set_state(NotificationTimeState.notification_time)
    
    await message.answer(
        "Now, enter the time at which you want to receive notifications.\n"
        "For example:\n"
        "8:00"
    )
    

@router.message(NotificationTimeState.notification_time)
async def process_notification_time(message: Message, state: FSMContext) -> None:
    user_info = await get_user_info(message)
    user_id, username = user_info.id, user_info.username
    
    new_time = message.text.strip()
    
    async with AsyncSessionLocal() as session:
        updated_user = await user_repo.update_user_time(
            session,
            user_id,
            username,
            new_time
        )

    if not updated_user:
        await message.answer(
            "⚠️ Invalid time format. Please enter time as HH:MM (e.g., 08:00)."
        )
        return

    await reschedule_user(user_id, message.bot)
    await message.answer(
        f"✅Great! Notification time set to {new_time}.\n"
        "You will start receiving daily digests of tech news based on your interests!"
    )
    await state.clear()