from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .jobs import notification_service
from app.database import user_repo

from datetime import datetime

# TODO: Enable automatic adjustment to the user's region
# TODO: Create a jobs store
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")