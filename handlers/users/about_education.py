from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.personalData import Education, MainMenu


@dp.message_handler(text=["Bosh Menu", "Orqaga"], state=Education.button)
async def about(message: types.Message, state: FSMContext):
    button = message.text
    if button == "Bosh Menu":
        await MainMenu.main_menu.set()
    elif button == "Orqaga":
        await MainMenu.main_menu.set()
