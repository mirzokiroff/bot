from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.languages import uz
from loader import dp
from states.personalData import MainMenu


@dp.message_handler(text=[uz.bosh_menu], state=MainMenu.main_menu)
async def main_menu(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text=uz.buyurtma_berish, callback_data='menu'))
    keyboard.row(InlineKeyboardButton(text=uz.biz_haqimizda, callback_data='about_us'),
                 InlineKeyboardButton(text=uz.buyurtmalarim, callback_data='my_orders'))
    keyboard.row(InlineKeyboardButton(text=uz.manzilimiz, callback_data='address'))
    keyboard.row(InlineKeyboardButton(text=uz.fikr_bildirish, callback_data='feedback'),
                 InlineKeyboardButton(text=uz.sozlamalar, callback_data='settings'))

    await message.answer("Buyurmani birga joylashtiramizmi? 🤗")
    await message.answer(
        "Buyurtma berishni boshlash uchun 🛒 Buyurtma qilish tugmasini bosing "
        "\n\nShuningdek, aksiyalarni ko'rishingiz va bizning filiallar bilan tanishishingiz mumkin"
        "\n\n\nhttps://telegra.ph/Taomnoma-04-03",
        reply_markup=keyboard)
    await MainMenu.menu.set()