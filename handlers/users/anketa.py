from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from django.utils import timezone

from handlers.languages import uz, ru
from handlers.users.phone_code import generate_confirmation_code, send_confirmation_code
from keyboards.default.keyboard import telefon_raqam_btn
from loader import dp, db
from states.personalData import PersonalData, Language
from math import radians, sin, cos, sqrt, atan2

import re

from utils.db_api.postgresql import Database

uzbekcha = "🇺🇿 O'zbekcha"
ruscha = "🇷🇺 Русский"


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c

    return distance


def find_nearest_restaurant(user_location, restaurant_locations):
    min_distance = float('inf')
    nearest_restaurant = None

    user_lat = user_location.latitude
    user_lon = user_location.longitude

    for restaurant in restaurant_locations:
        restaurant_lat = restaurant.latitude
        restaurant_lon = restaurant.longitude

        distance = calculate_distance(user_lat, user_lon, restaurant_lat, restaurant_lon)

        if distance < min_distance:
            min_distance = distance
            nearest_restaurant = restaurant

    return nearest_restaurant


def is_valid_name(name):
    if not re.match(r'^[a-zA-Zа-яА-Я\s\'\`\’]+$', name):  # noqa
        return False

    if len(name) < 2 or len(name) > 50:
        return False

    return True


def is_valid_phone_number(phone_number_for_call):
    if not re.match(r'^\+?998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$', phone_number_for_call):
        return False

    return True


@dp.message_handler(Text(equals=["🇺🇿 O'zbekcha", "🇷🇺 Русский"], ignore_case=True), state=Language.languages)
async def enter(message: types.Message, state: FSMContext):
    language = message.text

    await state.update_data(
        {'til': language}
    )

    if language == uzbekcha:
        await message.answer(uz.ism_sorash, reply_markup=types.ReplyKeyboardRemove())
    elif language == ruscha:
        await message.answer(ru.ism_sorash, reply_markup=types.ReplyKeyboardRemove())
    await PersonalData.fullname.set()


@dp.message_handler(state=PersonalData.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    data = await state.get_data()
    language = data.get('til')

    if language == uzbekcha:
        if not is_valid_name(fullname):
            await message.reply(uz.xato_ism)
            return

        await message.answer(uz.telefon_raqam, reply_markup=telefon_raqam_btn)
        await PersonalData.phone_number_for_call.set()
    elif language == ruscha:
        if not is_valid_name(fullname):
            await message.reply(ru.xato_ism)
            return

        await message.answer(ru.telefon_raqam, reply_markup=telefon_raqam_btn)
        await PersonalData.phone_number_for_call.set()

    await state.update_data(
        {'name': fullname}
    )


@dp.message_handler(state=PersonalData.phone_number_for_call, content_types=types.ContentType.CONTACT)
async def tasdiqlash_kod(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    language = data.get('til')

    # Telefon raqamini to'g'ri formatga olib kelish
    formatted_phone_number = f"+{phone_number}"

    await state.update_data({'phone_number': formatted_phone_number})

    db = Database()
    await db.create()

    confirmation_code = generate_confirmation_code()
    await state.update_data({'confirmation_code': confirmation_code})

    if language == uzbekcha:
        await message.answer(f"{uz.tasdiqlash_kod}", reply_markup=ReplyKeyboardRemove())
    elif language == ruscha:
        await message.answer(f"{ru.tasdiqlash_kod}", reply_markup=ReplyKeyboardRemove())

    # Foydalanuvchiga tasdiqlash kodini yuborish
    # await send_confirmation_code(confirmation_code, [formatted_phone_number])

    await PersonalData.confirm_data.set()


@dp.message_handler(state=PersonalData.confirm_data)
async def confirm_data(message: types.Message, state: FSMContext):
    confirm = message.text
    data = await state.get_data()
    language = data.get('til')
    confirmation_code = data.get('confirmation_code')

    if confirm == '0000':
        await message.answer("✅ Tasdiqlandi! \n\nEng yaqin filialni topish uchun lokatsiyangizni yuboring")
        await PersonalData.location.set()
    else:
        await message.answer("❌ Tasdiqlanmadi. Iltimos, tasdiqlash kodingizni tekshiring va qaytadan kiriting.")


@dp.message_handler(state=PersonalData.location, content_types=types.ContentType.LOCATION)
async def location_received(message: types.Message, state: FSMContext):
    location = message.location
    data = await state.get_data()
    language = data.get('til')
    name = data.get('name')
    phone_number = data.get('phone_number')
    confirmation_code = data.get('confirmation_code')

    await state.update_data(location=location)

    if location:
        await db.add_user(full_name=name, username=message.from_user.username, phone_number=phone_number,
                          telegram_id=message.from_user.id, language=language, confirmation_code=confirmation_code,
                          location=location)
    else:
        await message.answer("Iltimos, Lokatsiya to'g'ri yuborganingizga ishonch hosil qiling!")
    await state.finish()
