from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config.config import settings

# Инициализация бота
bot = Bot(
    token=settings.bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)