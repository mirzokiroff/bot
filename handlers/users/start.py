import asyncpg
from aiogram import types
from datetime import datetime
from loader import dp, db, bot
from data.config import ADMINS
from states.personalData import Language


@dp.message_handler(commands=['start'], state="*")
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username,
                                 date_joined=datetime.now())
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    # Adminga xabar beramiz
    count = await db.count_users()
    msg = (f"{message.from_user.full_name} bazaga qo'shildi.\n\n"
           f"Foydalanuvchi Ma'lumotlari:\n"
           f"Foydalanuvchi telegram id:{message.from_user.id}\n\n"
           f"Foydalanuvchi username: @{message.from_user.username}\n\n"
           f"Foydalanuvchi premium: {message.from_user.is_premium}\n\n"
           f"Bazada {count} ta foydalanuvchi bor.")
    await bot.send_message(chat_id=ADMINS[0], text=msg)
    await message.reply(
        f"Assalomu Alaykum! {message.from_user.full_name}\nExtra Education Center botiga xush kelibsiz! \n\n\n"
        f"Здравствуйте! {message.from_user.full_name}\nДобро пожаловать в бот Центра Extra!")
    if message.text == '/start':
        await message.answer("Tilni tanlang! \n\n\nВыберите ваш язык!",
                             reply_markup=types.ReplyKeyboardMarkup(
                                 keyboard=[
                                     [types.KeyboardButton(text="🇺🇿 O'zbekcha"),
                                      types.KeyboardButton(text="🇷🇺 Русский")]
                                 ],
                                 resize_keyboard=True
                             ))
        await Language.languages.set()

