from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.keyboard import til_tanlash_btn
from loader import dp
from states.personalData import Language


@dp.message_handler(commands=['start'], state="*")
async def bot_start(message: types.Message):
    await message.reply(
        f"Assalomu Alaykum! {message.from_user.full_name}\nRestaurant botiga xush kelibsiz!")

    if message.text == '/start':
        await message.answer(
            "Iltimos, Botdan foydalanish uchun Tilni tanlang\n\n"
            "Пожалуйста, выберите язык для использования бота",
            reply_markup=til_tanlash_btn)
        await Language.languages.set()
