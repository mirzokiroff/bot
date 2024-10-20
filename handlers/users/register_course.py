from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime
from handlers.languages import uz, ru

from loader import dp, db
from states.personalData import Register_Course, Courses, PersonalData, MainMenu

uzbekcha = "🇺🇿 O'zbekcha"
ruscha = "🇷🇺 Русский"


@dp.message_handler(
    text=[uz.kursga_royxatdan_otish, ru.kursga_royxatdan_otish, uz.bosh_menu, ru.bosh_menu, uz.orqaga, ru.orqaga],
    state=Register_Course.course_type)
async def register_to_course(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    language = data.get("til")
    if language == uzbekcha:
        if text == uz.kursga_royxatdan_otish:
            await message.answer("Kurs turini tanlang:", reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=uz.online), types.KeyboardButton(text=uz.offline)]
                ],
                resize_keyboard=True
            ))
            await PersonalData.activity.set()
        elif text == uz.bosh_menu:
            await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                    [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
            await MainMenu.menu.set()
        elif text == uz.orqaga:
            await Courses.course_selection.set()
    elif language == ruscha:
        if text == ru.kursga_royxatdan_otish:
            await message.answer("Выберите тип курса:", reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=ru.online), types.KeyboardButton(text=ru.offline)]
                ],
                resize_keyboard=True
            ))
            await PersonalData.activity.set()
        elif text == ru.bosh_menu:
            await message.answer(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                    [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
            await MainMenu.menu.set()
        elif text == ru.orqaga:
            await Courses.course_selection.set()


@dp.message_handler(lambda message: message.text in [uz.online, ru.online, uz.offline, ru.offline])
@dp.message_handler(state=PersonalData.activity)
async def enter_activity(message: types.Message, state: FSMContext):
    course_type = message.text
    data = await state.get_data()
    language = data.get("til")

    # Ma'lumotlarni saqlash
    await state.update_data(course_type=course_type)

    # Ma'lumotlarni tasdiqlash uchun so'rov jo'natamiz
    data = await state.get_data()
    course = data.get("course")
    course_type = data.get("course_type")
    name = data.get("name")
    phone_number = data.get("phone")
    phone_number2 = data.get("phone_number")
    activity = data.get("activity")

    if language == uzbekcha:
        await message.reply(
            f"Ismingiz: {name}\n"
            f"Telefon raqamingiz: {phone_number}\n"
            f"Qo'shimcha Telefon raqam: {phone_number2}\n"
            f"Faoliyat turi: {activity}\n"
            f"Kurs: {course}\n"
            f"Kurs turi: {course_type}\n"
            f"Ushbu ma'lumotlar to'g'ri ekanligini tasdiqlaysizmi?",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="HA"), types.KeyboardButton(text="YO'Q")]
                ],
                resize_keyboard=True
            ))
        await PersonalData.confirmm_data.set()
    elif language == ruscha:
        await message.reply(
            f"Ваше имя: {name}\n"
            f"Ваш номер телефона: {phone_number}\n"
            f"Ваш дополнительный номер телефона: {phone_number2}\n"
            f"Тип активности: {activity}\n"
            f"Курс: {course}\n"
            f"Тип курса: {course_type}\n"
            f"Вы подтверждаете, что эта информация верна?",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="ДА"), types.KeyboardButton(text="НЕТ")]
                ],
                resize_keyboard=True
            ))
        await PersonalData.confirmm_data.set()


@dp.message_handler(lambda message: message.text in ["HA", "YO'Q", "ДА", "НЕТ"], state=PersonalData.confirmm_data)
async def confirmm_data(message: types.Message, state: FSMContext):
    choice = message.text
    data = await state.get_data()
    language = data.get("til")

    if choice in ["HA", "ДА"]:
        # Ma'lumotlarni tasdiqlash
        data = await state.get_data()
        course = data.get("course")
        course_type = data.get("course_type")
        name = data.get("name")
        phone_number2 = data.get("phone_number")
        activity = data.get("activity")
	date_joined = datetime.now()

        # Ma'lumotlarni olish
        course_name = data.get("course_name")
        phone = data.get("phone")

        # Ma'lumotlarni bazaga saqlash
        await db.user_add_course(user_name=name, user_phone_number=phone, course_type=course_type,
                                 course_name=course_name, user_phone_number2=phone_number2, date_joined=date_joined)
        if language == uzbekcha:
            await message.answer(f"Ma'lumotlar tasdiqlandi!\n"
                                 f"Ism: {name}\n"
                                 f"Telefon raqam: {phone}\n"
                                 f"Qo'shimcha Telefon raqam: {phone_number2}\n"
                                 f"Faoliyat turi: {activity}\n"
                                 f"Kurs: {course}\n"
                                 f"Kurs turi: {course_type}\n\n"
                                 f"Ma'lumotlaringiz uchun rahmat!\n\n"
                                 f"Sizga tez orada administratorlarimiz aloqaga chiqishadi.",
                                 reply_markup=types.ReplyKeyboardMarkup(
                                     keyboard=[
                                         [types.KeyboardButton(text=uz.bosh_menu)],
                                     ],
                                     resize_keyboard=True
                                 ))
            await MainMenu.main_menu.set()
        elif language == ruscha:
            await message.answer(f"Данные проверены!\n"
                                 f"Имя: {name}\n"
                                 f"Номер телефона: {phone}\n"
                                 f"Дополнительный номер телефона: {phone_number2}\n"
                                 f"Тип активности: {activity}\n"
                                 f"Курс: {course}\n"
                                 f"Тип курса: {course_type}\n\n"
                                 f"Спасибо за вашу информацию!\n\n"
                                 f"Наши администраторы свяжутся с вами в ближайшее время.",
                                 reply_markup=types.ReplyKeyboardMarkup(
                                     keyboard=[
                                         [types.KeyboardButton(text=ru.bosh_menu)],
                                     ],
                                     resize_keyboard=True
                                 ))
            await MainMenu.main_menu.set()
    else:
        if language == uzbekcha:
            await message.answer("Ma'lumotlarni qayta kiriting va Kerakli amaliyotlarni boshidan bajaring")
            await message.answer("To'liq ismingizni kiriting")
            await PersonalData.fullname.set()
        elif language == ruscha:
            await message.answer("Повторно введите информацию и выполните необходимые операции с начала.")
            await message.answer("Введите свое полное имя")
            await PersonalData.fullname.set()
