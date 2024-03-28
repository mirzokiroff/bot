from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.languages import uz, ru
from loader import dp
from states.personalData import Language, MainMenu, PersonalData

uzbekcha = "🇺🇿 O'zbekcha"
ruscha = "🇷🇺 Русский"


@dp.message_handler(commands=['language'], state="*")
async def select_language(message: types.Message):
    language = message.text

    if language == '/language':
        await message.answer("Tilni tanlang! \n\n\nВыберите ваш язык!",
                             reply_markup=types.ReplyKeyboardMarkup(
                                 keyboard=[
                                     [types.KeyboardButton(text="🇺🇿 O'zbekcha"),
                                      types.KeyboardButton(text="🇷🇺 Русский")]
                                 ],
                                 resize_keyboard=True
                             ))
        await Language.select_language.set()


@dp.message_handler(Text(equals=['🇺🇿 O\'zbekcha', '🇷🇺 Русский']), state=Language.select_language)
async def select_language(message: types.Message, state: FSMContext):
    language = message.text
    await state.update_data({'til': language})
    data = await state.get_data()

    # Tasdiqlash tugmasi yuborish
    if language == uzbekcha:
        await message.reply(
            f"Ismingiz: {data.get('name')}\nQo'shimcha Telefon raqamingiz: {data.get('phone_number')}\n"
            f"Telefon raqamingiz: {data.get('phone')}\nFaoliyat turi: {data.get('activity')}\n"
            f"Tanlagan tilingiz: {language}\n\nUshbu ma'lumotlar to'g'ri ekanligini tasdiqlaysizmi?",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[[types.KeyboardButton(text="HA"), types.KeyboardButton(text="YO'Q")]],
                resize_keyboard=True
            ))
    elif language == ruscha:
        await message.reply(
            f"Ваше имя: {data.get('name')}\n"
            f"Ваш дополнительный номер телефона: {data.get('phone_number')}\n"
            f"Ваш номер телефона: {data.get('phone')}\n"
            f"Тип активности: {data.get('activity')}\n"
            f"Выбранный вами язык: {language}"
            f"\n\nВы подтверждаете, что эта информация верна?",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]], resize_keyboard=True
            ))

    await PersonalData.confirm_data.set()
