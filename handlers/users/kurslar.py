import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.languages import uz, ru
from loader import dp, db
from states.personalData import Courses, Register_Course, MainMenu

uzbekcha = "🇺🇿 O'zbekcha"
ruscha = "🇷🇺 Русский"


@dp.message_handler(state=Courses.course_selection)
async def select_course(message: types.Message, state: FSMContext):
    course_name = message.text
    data = await state.get_data()
    language = data.get('til')

    await state.update_data(
        {'course': course_name}
    )

    courses = await db.select_all_courses()

    if language == uzbekcha:
        if course_name in [course['course_name'] for course in courses] or course_name == uz.orqaga:
            await state.update_data({'course_name': course_name})
            await message.reply("Kurs turini tanlang:", reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=uz.online), types.KeyboardButton(text=uz.offline)],
                    [types.KeyboardButton(text=uz.bosh_menu), types.KeyboardButton(text=uz.orqaga)]
                ],
                resize_keyboard=True
            ))
            await Courses.course_video.set()

        elif course_name == uz.bosh_menu:
            await message.reply(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                    [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
            await MainMenu.menu.set()
        else:
            await message.reply("Noto'g'ri tanlov, Iltimos kurs nomini to'g'ri kiriting !!!")
    elif language == ruscha:
        if course_name in [course['course_name'] for course in courses] or course_name == ru.orqaga:
            await state.update_data({'course_name': course_name})
            await message.reply("Выберите тип курса:", reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=ru.online), types.KeyboardButton(text=ru.offline)],
                    [types.KeyboardButton(text=ru.bosh_menu), types.KeyboardButton(text=ru.orqaga)]
                ],
                resize_keyboard=True
            ))
            await Courses.course_video.set()

        elif course_name == ru.bosh_menu:
            await message.reply(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                    [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
            await MainMenu.menu.set()
        else:
            await message.reply("Неправильный выбор, введите правильное название курса!!!")


@dp.message_handler(
    text=[uz.online, uz.offline, ru.online, ru.offline, uz.bosh_menu, ru.bosh_menu, uz.orqaga, ru.orqaga],
    state=Courses.course_video)
async def select_course_type_eng(message: types.Message, state: FSMContext):
    course_type = message.text
    data = await state.get_data()
    language = data.get('til')

    await state.update_data(
        {'course_type': course_type}
    )

    if language == uzbekcha:
        if course_type == uz.bosh_menu:
            await message.reply(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                    [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
            await MainMenu.menu.set()
        elif course_type == uz.orqaga:
            courses = await db.select_all_courses()  # noqa

            courses_keyboard = []
            row = []
            for course in courses:
                course_name = course["course_name"]
                row.append(types.KeyboardButton(text=course_name))
                if len(row) == 3:
                    courses_keyboard.append(row)
                    row = []

            if row:
                courses_keyboard.append(row)

            courses_keyboard.append([types.KeyboardButton(text=uz.bosh_menu)])

            await message.reply("Siz Kurslar bo'limini tanladingiz!\n\nIltimos quyidagi kurslardan birini tanlang!",
                                reply_markup=types.ReplyKeyboardMarkup(
                                    keyboard=courses_keyboard,
                                    resize_keyboard=True
                                ))
            await Courses.course_selection.set()

        else:
            await message.answer(
                text="Bu yerda siz Kurs haqida ma'lumotlarga ega bo'lishingiz mumkun, Iltimos biroz kuting",
                reply_markup=types.ReplyKeyboardRemove())

            course_name = data.get('course_name')

            selected_course = await db.select_course(course_name=course_name)

            course_id = selected_course['id']

            course_media = await db.select_all_courses_media()

            photos = []
            pdfs = []

            media_root = '/var/www/bot/extra/media/'

            if course_name:
                for media in course_media:  # noqa
                    if media['media_id'] == course_id:
                        full_photo_path = os.path.join(media_root, media['course_photo'])
                        full_pdf_path = os.path.join(media_root, media['course_pdf'])

                        if media['course_video']:
                            caption = media['course_text'] if media['course_text'] else ""
                            await message.answer_video(video=media['course_video'], caption=caption)

                        if os.path.exists(full_photo_path) and media['course_photo']:
                            photos.append(full_photo_path)

                        if os.path.exists(full_pdf_path) and media['course_pdf']:
                            pdfs.append(full_pdf_path)

                if photos:
                    for photo in photos:
                        await message.answer_photo(photo=open(photo, 'rb'))

                if pdfs:
                    for pdf in pdfs:
                        await message.answer_document(document=open(pdf, 'rb'))

                await message.reply(f"{course_name} kursining {course_type} turidan ro'yxatdan o'tishingiz mumkun",
                                    reply_markup=types.ReplyKeyboardMarkup(
                                        keyboard=[
                                            [types.KeyboardButton(text=uz.kursga_royxatdan_otish)],
                                            [types.KeyboardButton(text=uz.bosh_menu)]
                                        ], resize_keyboard=True
                                    ))
                await Register_Course.course_type.set()
            else:
                await message.reply("Tanlangan kurs topilmadi, iltimos boshqa kurs nomini kiriting!!!")
                await message.reply(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                    keyboard=[
                        [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                        [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                    ],
                    resize_keyboard=True
                ))
                await MainMenu.menu.set()

    elif language == ruscha:
        if course_type == ru.bosh_menu:
            await message.reply(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                    [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))
            await MainMenu.menu.set()
        elif course_type == ru.orqaga:
            courses = await db.select_all_courses()  # noqa

            courses_keyboard = []
            row = []
            for course in courses:
                course_name = course["course_name"]
                row.append(types.KeyboardButton(text=course_name))
                if len(row) == 3:
                    courses_keyboard.append(row)
                    row = []

            if row:
                courses_keyboard.append(row)

            courses_keyboard.append([types.KeyboardButton(text=ru.bosh_menu)])

            await message.reply("Вы выбрали раздел «Курсы»!\n\nПожалуйста, выберите один из курсов ниже!",
                                reply_markup=types.ReplyKeyboardMarkup(
                                    keyboard=courses_keyboard,
                                    resize_keyboard=True
                                ))
            await Courses.course_selection.set()

        else:
            await message.answer(text="Здесь вы можете получить информацию о курсе, Пожалуйста, подождите",
                                 reply_markup=types.ReplyKeyboardRemove())

            course_name = data.get('course_name')

            selected_course = await db.select_course(course_name=course_name)

            course_id = selected_course['id']

            course_media = await db.select_all_courses_media()

            photos = []
            pdfs = []

            media_root = '/var/www/bot/extra/media/'

            if course_name:
                for media in course_media:  # noqa
                    if media['media_id'] == course_id:

                        full_photo_path = os.path.join(media_root, media['course_photo'])
                        full_pdf_path = os.path.join(media_root, media['course_pdf'])

                        if media['course_video']:
                            caption = media['course_text'] if media['course_text'] else ""
                            await message.answer_video(video=media['course_video'], caption=caption)

                        if os.path.exists(full_photo_path) and media['course_photo']:
                            photos.append(full_photo_path)

                        if os.path.exists(full_pdf_path) and media['course_pdf']:
                            pdfs.append(full_pdf_path)

                if photos:
                    for photo in photos:
                        await message.answer_photo(photo=open(photo, 'rb'))

                if pdfs:
                    for pdf in pdfs:
                        await message.answer_document(document=open(pdf, 'rb'))

                await message.reply(f"Вы можете зарегистрироваться на курс {course_name} типа {course_type}",
                                    reply_markup=types.ReplyKeyboardMarkup(
                                        keyboard=[
                                            [types.KeyboardButton(text=ru.kursga_royxatdan_otish)],
                                            [types.KeyboardButton(text=ru.bosh_menu)]
                                        ], resize_keyboard=True
                                    ))
                await Register_Course.course_type.set()
            else:
                await message.reply("Выбранный курс не найден. Введите другое название курса!!!")
                await message.reply(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                    keyboard=[
                        [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                        [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                    ],
                    resize_keyboard=True
                ))
                await MainMenu.menu.set()
