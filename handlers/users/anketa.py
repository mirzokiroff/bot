from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.languages import uz, ru
from loader import dp, db
from states.personalData import PersonalData, MainMenu, Language

import re

uzbekcha = "🇺🇿 O'zbekcha"
ruscha = "🇷🇺 Русский"


def is_valid_name(name):
    if not re.match(r'^[a-zA-Zа-яА-Я\s\'\`\’]+$', name):
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

        await message.reply(uz.aloqa_raqam)
    elif language == ruscha:
        if not is_valid_name(fullname):
            await message.reply(ru.xato_ism)
            return

        await message.reply(ru.aloqa_raqam)

    await state.update_data(
        {'name': fullname}
    )

    await PersonalData.phone_number_for_call.set()


@dp.message_handler(state=PersonalData.phone_number_for_call)
async def answer_phone_number2(message: types.Message, state: FSMContext):
    phone_number_for_call = message.text
    data = await state.get_data()
    language = data.get('til')

    if language == uzbekcha:
        if not is_valid_phone_number(phone_number_for_call):
            await message.reply(uz.xato_aloqa_raqam)
            return

        await message.answer(uz.telefon_raqam, reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Telefon raqam", request_contact=True)]],
            resize_keyboard=True
        ))
    elif language == ruscha:
        if not is_valid_phone_number(phone_number_for_call):
            await message.reply(ru.xato_aloqa_raqam)
            return

        await message.answer(ru.telefon_raqam, reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Ваш номер телефона", request_contact=True)]],
            resize_keyboard=True
        ))

    await state.update_data(
        {'phone_number': phone_number_for_call}
    )

    await PersonalData.phone_number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=PersonalData.phone_number)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    data = await state.get_data()
    language = data.get('til')

    await state.update_data({'phone': phone})

    if language == uzbekcha:
        await message.answer(uz.faoliyat_turi, reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Talaba"), types.KeyboardButton(text="Maktab o'quvchisi")],
                [types.KeyboardButton(text="Tashkilot xodimi"), types.KeyboardButton(text="Vaqtincha ishsiz")]
            ],
            resize_keyboard=True
        ))
    elif language == ruscha:
        await message.answer(ru.faoliyat_turi, reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Студент"), types.KeyboardButton(text="Школьник")],
                [types.KeyboardButton(text="Работник организации"), types.KeyboardButton(text="Временно безработный")]
            ],
            resize_keyboard=True
        ))

    await PersonalData.activity.set()


@dp.message_handler(
    lambda message: message.text in ["Talaba", "Maktab o'quvchisi", "Tashkilot xodimi", "Vaqtincha ishsiz",
                                     "Временно безработный", "Студент", "Школьник", "Работник организации"],
    state=PersonalData.activity)
async def select_activity(message: types.Message, state: FSMContext):
    activity = message.text
    data = await state.get_data()
    language = data.get('til')

    await state.update_data({'activity': activity})

    # Tasdiqlash tugmasi yuborish
    if language == uzbekcha:
        await message.reply(
            f"Ismingiz: {data.get('name')}\nQo'shimcha Telefon raqamingiz: {data.get('phone_number')}\n"
            f"Telefon raqamingiz: {data.get('phone')}\nFaoliyat turi: {activity}\n"
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
            f"Тип активности: {activity}\n"
            f"Выбранный вами язык: {language}"
            f"\n\nВы подтверждаете, что эта информация верна?",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]], resize_keyboard=True
            ))

    await PersonalData.confirm_data.set()


@dp.message_handler(lambda message: message.text in ["HA", "YO'Q", "Да", "Нет"], state=PersonalData.confirm_data)
async def confirmm_data(message: types.Message, state: FSMContext):
    choice = message.text
    data = await state.get_data()
    language = data.get("til")
    if choice in ["HA", "Да"]:
        name = data.get("name")
        phone2 = data.get("phone_number")
        phone = data.get("phone")
        activity = data.get("activity")

        # Ma'lumotlarni bazaga saqlash
        await db.add_user(full_name=name, username=message.from_user.username, phone_number=phone, phone_number2=phone2,
                          activity=activity, telegram_id=message.from_user.id, language=language)

        if language == uzbekcha:
            await message.answer(
                f"Ma'lumotlar tasdiqlandi:\n"
                f"Ismingiz: {name}\n"
                f"Qo'shimcha Telefon raqamingiz: {phone2}\n"
                f"Telefon raqamingiz: {phone}\n"
                f"Faoliyat turi: {activity}\n"
                f"Tanlagan tilingiz: {language}\n\n"
                f"Ma'lumotlaringiz uchun rahmat! Bosh menyu bilan tanishishingiz mumkun!",
                reply_markup=types.ReplyKeyboardRemove())
            await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                    [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
        elif language == ruscha:
            await message.answer(
                f"Информация проверена:\n"
                f"Ваше имя: {name}\n"
                f"Ваш дополнительный номер телефона: {phone2}\n"
                f"Ваш номер телефона: {phone}\n"
                f"Тип активности: {activity}\n\n"
                f"Спасибо за информацию! Пожалуйста, загляните в главное меню!",
                reply_markup=types.ReplyKeyboardRemove())
            await message.answer(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                    [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
        await MainMenu.menu.set()
    elif choice in ["YO'Q", "Нет"]:
        if language == uzbekcha:
            await message.reply(uz.xato_malumot)
            await message.answer(uz.ism_sorash)
        elif language == ruscha:
            await message.reply(ru.xato_malumot)
            await message.answer(ru.ism_sorash)
        await PersonalData.fullname.set()
