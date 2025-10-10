from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from asyncio import run

from app.core import logger, settings


async def on_startup() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.include_routers(
        
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"The code finished with an error: {e}")
        return None
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        run(on_startup())
        logger.info("Bot started successfully!")
    except KeyboardInterrupt:
        logger.info("Bot stopped manually.")