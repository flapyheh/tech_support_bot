from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.lexicon.lexicon import RU

keyboard_user = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text= RU['user_help_btn'], callback_data= RU['user_help_call'])]]
    )