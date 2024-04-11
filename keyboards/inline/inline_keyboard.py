from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.languages import uz
from loader import dp

MenuStart = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=uz.buyurtma_berish, callback_data="buyurtma_berish"),
        ],
        [
            InlineKeyboardButton(text=uz.buyurtmalarim, callback_data="buyurmalarim"),
            InlineKeyboardButton(text=uz.biz_haqimizda, callback_data="biz_haqimizda"),
        ],
        [
            InlineKeyboardButton(text=uz.manzilimiz, callback_data="manzilimiz"),
        ],
        [
            InlineKeyboardButton(text=uz.fikr_bildirish, callback_data='fikr_bildirish'),
            InlineKeyboardButton(text=uz.sozlamalar, callback_data='sozlamalar'),
        ],
    ])

MainMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=uz.bosh_menu, callback_data="bosh_menu")]
    ]
)

Settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=uz.uz, callback_data="til"),
         InlineKeyboardButton(text=uz.telefon, callback_data="telefon")],
        [InlineKeyboardButton(text=uz.bosh_menu, callback_data="bosh_menu")]
    ]
)
