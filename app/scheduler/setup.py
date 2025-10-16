from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .jobs import notification_service
from app.database import user_repo

from datetime import datetime

# TODO: Enable automatic adjustment to the user's region
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler.add_job(
    notification_service.send_daily_news,
    trigger="cron",
    hour=datetime.now().hour,
    minute=datetime.now().minute + 1,
    start_date=datetime.now(),
)