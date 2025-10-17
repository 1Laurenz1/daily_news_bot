from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from asyncio import run

from app.core import logger, settings
from app.database import engine
from app.bot import start
from app.scheduler.setup import (
    start_scheduler,
    shutdown_scheduler,
    schedule_all_users,
)


async def on_shutdown() -> None:
    await engine.dispose()
    logger.info("engine was successfully disposed!")


async def on_startup() -> None:
    logger.info("Bot starting...")
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.include_routers(
        start.router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started successfully!")
    
    # Start scheduler and load jobs from DB
    start_scheduler()
    await schedule_all_users(bot)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"The code finished with an error: {e}")
        return None
    finally:
        shutdown_scheduler()
        await bot.session.close()
        await on_shutdown()


if __name__ == '__main__':
    try:
        run(on_startup())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually.")