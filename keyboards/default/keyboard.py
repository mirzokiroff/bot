from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from handlers.languages import uz
from loader import dp
from states.personalData import MainMenu


@dp.message_handler(text=[uz.bosh_menu], state=MainMenu.main_menu)
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
        keyboard=[
            [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
            [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
        ],
        resize_keyboard=True
    ))
    await MainMenu.menu.set()


buyurtma_berish_btn = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=uz.eltib_berish), types.KeyboardButton(text=uz.borib_olish)],
        [types.KeyboardButton(text=uz.orqaga)]
    ], resize_keyboard=True
)

telefon_raqam_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=uz.telefon_raqam_y, request_contact=True)]
    ], resize_keyboard=True
)

til_tanlash_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=uz.uz), KeyboardButton(text=uz.ru)]
    ], resize_keyboard=True
)
