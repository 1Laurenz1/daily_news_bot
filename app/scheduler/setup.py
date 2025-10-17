from __future__ import annotations

from datetime import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlalchemy import select

from aiogram import Bot

from .jobs import notif_serv
from app.core import logger
from app.database import AsyncSessionLocal, User


# TODO: Enable automatic adjustment to the user's region per-user
# TODO: Create a persistent job store (e.g., Redis or DB) if needed
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


def _job_id_for_user(user_id: int) -> str:
    return f"daily_digest_user_{user_id}"


def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.start()
        logger.info("APScheduler started")


def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped")


def remove_user_job(user_id: int) -> None:
    job_id = _job_id_for_user(user_id)
    job = scheduler.get_job(job_id)
    if job:
        scheduler.remove_job(job_id)
        logger.info(f"Removed existing job for user {user_id}")


def schedule_user_job(user_id: int, notification_time: time, bot: Bot) -> None:
    """Schedule (or replace) a daily digest job for a specific user."""
    if not notification_time:
        return

    job_id = _job_id_for_user(user_id)

    trigger = CronTrigger(
        hour=notification_time.hour,
        minute=notification_time.minute,
        timezone=scheduler.timezone,
    )

    scheduler.add_job(
        func=notif_serv.send_daily_news_for_user,  # async function
        trigger=trigger,
        args=[user_id],
        kwargs={"bot": bot},
        id=job_id,
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=3600,  # 1h
        max_instances=1,
    )

    logger.info(
        f"Scheduled daily digest for user {user_id} at "
        f"{notification_time.strftime('%H:%M')} ({scheduler.timezone})"
    )


async def schedule_all_users(bot: Bot) -> None:
    """Load all users with a notification_time and schedule their jobs."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.notification_time.isnot(None))
        )
        users = list(result.scalars().all())

    if not users:
        logger.info("No users with notification_time to schedule")
        return

    for user in users:
        schedule_user_job(user.user_id, user.notification_time, bot)


async def reschedule_user(user_id: int, bot: Bot) -> None:
    """Fetch user from DB and schedule their job (replace if exists)."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

    if not user or not user.notification_time:
        remove_user_job(user_id)
        logger.info(f"User {user_id} has no notification_time; no job scheduled")
        return

    schedule_user_job(user_id, user.notification_time, bot)