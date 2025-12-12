import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db
from handlers import admin_router, voting_router

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    """Asosiy funksiya"""
    
    # Tokenni tekshirish
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return
    
    # Ma'lumotlar bazasini yaratish
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor")
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )
    dp = Dispatcher()
    
    # Routerlarni ulash
    dp.include_router(admin_router)
    dp.include_router(voting_router)
    
    logger.info("Bot ishga tushmoqda...")
    
    try:
        # Webhook o'chirish (agar mavjud bo'lsa)
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Botni ishga tushirish
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
