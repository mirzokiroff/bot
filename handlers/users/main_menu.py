import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.languages import uz, ru
from loader import dp, db, bot
from states.personalData import MainMenu, Courses

uzbekcha = "🇺🇿 O'zbekcha"
ruscha = "🇷🇺 Русский"


@dp.message_handler(text=[uz.bosh_menu, ru.bosh_menu], state=MainMenu.main_menu)
async def main_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('til')

    if language == uzbekcha:
        await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
            keyboard=[
                [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
            ],
            resize_keyboard=True
        ))
        await MainMenu.menu.set()
    elif language == ruscha:
        await message.answer(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
            keyboard=[
                [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
            ],
            resize_keyboard=True
        ))
        await MainMenu.menu.set()


@dp.message_handler(
    lambda message: message.text in [uz.kurslar, uz.manzil, uz.markaz_haqida, uz.biz_bn_aloqa, ru.kurslar, ru.manzil,
                                     ru.biz_bn_aloqa, ru.markaz_haqida], state=MainMenu.menu)
async def menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('til')

    if language == uzbekcha:
        if message.text == uz.kurslar:
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
                                    resize_keyboard=True, row_width=True
                                ))
            await Courses.course_selection.set()

        elif message.text == uz.markaz_haqida:

            await message.answer(text=uz.oquv_markaz_haqida_bilish, reply_markup=types.ReplyKeyboardRemove())

            about_edu_data = await db.select_all_edu()

            about_edu_data_media = await db.select_all_edu_media()

            if about_edu_data and about_edu_data_media:

                video_group = types.MediaGroup()

                photo_group = types.MediaGroup()

                pdf_group = types.MediaGroup()

                edu_photo_paths = []

                for edu_info in about_edu_data:

                    for edu_media in about_edu_data_media:

                        if edu_info['id'] == edu_media['media_id']:

                            media_root = '/Users/user/PycharmProjects/aiogram-bot-template/extra/media'

                            video_path = os.path.join(media_root, edu_media['video'])
                            photo_path = os.path.join(media_root, edu_media['photo'])
                            pdf_path = os.path.join(media_root, edu_media['pdf_file'])
                            edu_photo = os.path.join(media_root, edu_info['edu_photo'])

                            if os.path.exists(video_path) and edu_media['video']:
                                video_group.attach_video(types.InputFile(video_path))

                            if os.path.exists(photo_path) and edu_media['photo']:
                                photo_group.attach_photo(types.InputFile(photo_path), caption=edu_info['description'])

                            if os.path.exists(pdf_path) and edu_media['pdf_file']:
                                pdf_group.attach_document(types.InputFile(pdf_path))

                            if os.path.exists(edu_photo) and edu_info['edu_photo']:
                                edu_photo_paths.append(edu_photo)

                if len(video_group.media) > 0:
                    await bot.send_media_group(message.chat.id, media=video_group)

                if len(photo_group.media) > 0:
                    await bot.send_media_group(message.chat.id, media=photo_group)

                if edu_photo_paths:
                    await message.answer_photo(photo=open(edu_photo_paths[0], 'rb'),
                                               caption=edu_info['description'])  # noqa

                if len(pdf_group.media) > 0:
                    await bot.send_media_group(message.chat.id, media=pdf_group)

                await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa

                    keyboard=[

                        [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],

                        [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],

                    ],

                    resize_keyboard=True

                ))

                await MainMenu.menu.set()

            else:

                await message.reply("O'quv markaz haqida ma'lumot topilmadi.")

                await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                    keyboard=[
                        [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                        [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                    ],
                    resize_keyboard=True
                ))
                await MainMenu.menu.set()

        elif message.text == uz.biz_bn_aloqa:

            await message.answer(text="Bu yerda siz O'quv Markaz bilan bog'lanishingiz mumkun",

                                 reply_markup=types.ReplyKeyboardRemove())

            contact_us_data = await db.select_contact_us()

            if contact_us_data:

                phone_numbers = []  # noqa

                telegram_admins = []

                telegram_channels = []

                instagrams = []

                you_tubes = []

                emails = []

                for contact_info in contact_us_data:

                    if contact_info['phone_number'] and contact_info['phone_number'] not in phone_numbers:
                        phone_numbers.append(contact_info['phone_number'])

                    if contact_info['telegram_admin'] and contact_info['telegram_admin'] not in telegram_admins:
                        telegram_admins.append(contact_info['telegram_admin'])

                    if contact_info['telegram_chanel'] and contact_info['telegram_chanel'] not in telegram_channels:
                        telegram_channels.append(contact_info['telegram_chanel'])

                    if contact_info['instagram'] and contact_info['instagram'] not in instagrams:
                        instagrams.append(contact_info['instagram'])

                    if contact_info['you_tube'] and contact_info['you_tube'] not in you_tubes:
                        you_tubes.append(contact_info['you_tube'])

                    if contact_info['email'] and contact_info['email'] not in emails:
                        emails.append(contact_info['email'])

                contact_message = ""

                if phone_numbers:
                    contact_message += f"📞 Telefon raqami: {', '.join(phone_numbers)}\n\n"

                if telegram_admins:
                    contact_message += f"👩‍💼 Telegram Admin: {', '.join(telegram_admins)}\n\n"

                if telegram_channels:
                    contact_message += f"📡 Telegram Kanal: {', '.join(telegram_channels)}\n\n"

                if instagrams:
                    contact_message += f"📷 Instagram: {', '.join(instagrams)}\n\n"

                if you_tubes:
                    contact_message += f"🎥 YouTube: {', '.join(you_tubes)}\n\n"

                if emails:
                    contact_message += f"📧 Email: {', '.join(emails)}\n\n"

                await message.answer(text=contact_message)

            else:

                await message.reply("Biz bilan bog'lanish uchun ma'lumotlar topilmadi.")

            await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa

                keyboard=[

                    [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],

                    [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],

                ],

                resize_keyboard=True

            ))

            await MainMenu.menu.set()

        elif message.text == uz.manzil:

            await message.answer(text="Bu yerda siz O'quv Markaz manzilini olishingiz mumkun",
                                 reply_markup=types.ReplyKeyboardRemove())

            location_data = await db.select_location_edu()

            if location_data:

                for location_info in location_data:

                    location_latitude = location_info['location_latitude']  # noqa

                    location_longitude = location_info['location_longitude']

                    location_text = location_info['location_text']

                    location_video = location_info['location_video']

                    if location_text:
                        await message.answer(text=location_text)

                    await message.answer_location(latitude=location_latitude, longitude=location_longitude)

                    if location_video:

                        video_path = os.path.join('/var/www/bot/extra/media/',
                                                  location_video)

                        if os.path.exists(video_path):
                            await message.answer_video(video=open(video_path, 'rb'))

                await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                    keyboard=[
                        [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                        [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                    ],
                    resize_keyboard=True
                ))
                await MainMenu.menu.set()

            else:

                await message.reply("Manzilimiz haqida ma'lumot topilmadi.")

                await message.answer(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                    keyboard=[
                        [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                        [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
                    ],
                    resize_keyboard=True
                ))
                await MainMenu.menu.set()

        else:
            await message.reply("Noto'g'ri tanlov! Iltimos, bosh menudan tanlang.")

        #########################################################################################################  # noqa

    elif language == ruscha:
        if message.text == ru.kurslar:
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

            await message.reply(ru.kurslar, reply_markup=types.ReplyKeyboardMarkup(
                keyboard=courses_keyboard,
                resize_keyboard=True, row_width=True
            ))
            await Courses.course_selection.set()

        elif message.text == ru.manzil:
            await message.answer(text=ru.manzil_haqida_bilish,
                                 reply_markup=types.ReplyKeyboardRemove())

            location_data = await db.select_location_edu()  # noqa

            if location_data:

                for location_info in location_data:

                    location_latitude = location_info['location_latitude']  # noqa

                    location_longitude = location_info['location_longitude']

                    location_text = location_info['location_text']

                    location_video = location_info['location_video']

                    if location_text:
                        await message.answer(text=location_text)

                    await message.answer_location(latitude=location_latitude, longitude=location_longitude)

                    if location_video:

                        video_path = os.path.join('/var/www/bot/extra/media/',
                                                  location_video)

                        if os.path.exists(video_path):
                            await message.answer_video(video=open(video_path, 'rb'))

                await message.answer(text=ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                    keyboard=[
                        [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                        [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                    ],
                    resize_keyboard=True
                ))
                await MainMenu.menu.set()

            else:

                await message.reply("Никакой информации о нашем адресе не обнаружено.")

        elif message.text == ru.markaz_haqida:

            await message.answer(text=ru.oquv_markaz_haqida_bilish, reply_markup=types.ReplyKeyboardRemove())  # noqa

            about_edu_data = await db.select_all_edu()

            about_edu_data_media = await db.select_all_edu_media()

            if about_edu_data and about_edu_data_media:

                video_group = types.MediaGroup()

                photo_group = types.MediaGroup()

                pdf_group = types.MediaGroup()

                edu_photo_paths = []

                for edu_info in about_edu_data:

                    for edu_media in about_edu_data_media:

                        if edu_info['id'] == edu_media['media_id']:

                            video_path = os.path.join('/Users/user/PycharmProjects/aiogram-bot-template/extra/media',

                                                      edu_media['video'])

                            photo_path = os.path.join('/Users/user/PycharmProjects/aiogram-bot-template/extra/media',

                                                      edu_media['photo'])

                            pdf_path = os.path.join('/Users/user/PycharmProjects/aiogram-bot-template/extra/media',

                                                    edu_media['pdf_file'])

                            edu_photo = os.path.join('/Users/user/PycharmProjects/aiogram-bot-template/extra/media',

                                                     edu_info['edu_photo'])

                            if os.path.exists(video_path) and edu_media['video']:
                                video_group.attach_video(types.InputFile(video_path))

                            if os.path.exists(photo_path) and edu_media['photo']:
                                photo_group.attach_photo(types.InputFile(photo_path), caption=edu_info['description'])

                            if os.path.exists(pdf_path) and edu_media['pdf_file']:
                                pdf_group.attach_document(types.InputFile(pdf_path))

                            if os.path.exists(edu_photo) and edu_info['edu_photo']:
                                edu_photo_paths.append(edu_photo)

                if len(video_group.media) > 0:
                    await bot.send_media_group(message.chat.id, media=video_group)

                if len(photo_group.media) > 0:
                    await bot.send_media_group(message.chat.id, media=photo_group)

                if edu_photo_paths:
                    await message.answer_photo(photo=open(edu_photo_paths[0], 'rb'),

                                               caption=edu_info['description'])  # noqa

                if len(pdf_group.media) > 0:
                    await bot.send_media_group(message.chat.id, media=pdf_group)

                await message.answer(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(

                    keyboard=[

                        [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],

                        [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],

                    ],

                    resize_keyboard=True

                ))

                await MainMenu.menu.set()

            else:

                await message.reply("Информации об учебном центре не обнаружено.")

                await message.answer(ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(

                    keyboard=[

                        [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],

                        [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],

                    ],

                    resize_keyboard=True

                ))

                await MainMenu.menu.set()

        elif message.text == ru.biz_bn_aloqa:
            await message.answer(text=ru.aloqa_haqida_bilish,
                                 reply_markup=types.ReplyKeyboardRemove())

            contact_us_data = await db.select_contact_us()

            if contact_us_data:

                phone_numbers = []  # noqa

                telegram_admins = []

                telegram_channels = []

                instagrams = []

                you_tubes = []

                emails = []

                for contact_info in contact_us_data:

                    if contact_info['phone_number'] and contact_info['phone_number'] not in phone_numbers:
                        phone_numbers.append(contact_info['phone_number'])

                    if contact_info['telegram_admin'] and contact_info['telegram_admin'] not in telegram_admins:
                        telegram_admins.append(contact_info['telegram_admin'])

                    if contact_info['telegram_chanel'] and contact_info['telegram_chanel'] not in telegram_channels:
                        telegram_channels.append(contact_info['telegram_chanel'])

                    if contact_info['instagram'] and contact_info['instagram'] not in instagrams:
                        instagrams.append(contact_info['instagram'])

                    if contact_info['you_tube'] and contact_info['you_tube'] not in you_tubes:
                        you_tubes.append(contact_info['you_tube'])

                    if contact_info['email'] and contact_info['email'] not in emails:
                        emails.append(contact_info['email'])

                contact_message = ""

                if phone_numbers:
                    contact_message += f"📞 Номер телефона: {', '.join(phone_numbers)}\n\n"

                if telegram_admins:
                    contact_message += f"👩‍💼 Администратор телеграммы: {', '.join(telegram_admins)}\n\n"

                if telegram_channels:
                    contact_message += f"📡 Телеграм-канал: {', '.join(telegram_channels)}\n\n"

                if instagrams:
                    contact_message += f"📷 Инстаграм: {', '.join(instagrams)}\n\n"

                if you_tubes:
                    contact_message += f"🎥 YouTube: {', '.join(you_tubes)}\n\n"

                if emails:
                    contact_message += f"📧 Электронная почта: {', '.join(emails)}\n\n"

                await message.answer(text=contact_message)

            else:

                await message.reply("Контактная информация не найдена.")

            await message.answer(text=ru.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
                keyboard=[
                    [types.KeyboardButton(text=ru.kurslar), types.KeyboardButton(text=ru.markaz_haqida)],
                    [types.KeyboardButton(text=ru.manzil), types.KeyboardButton(text=ru.biz_bn_aloqa)],
                ],
                resize_keyboard=True
            ))

            await MainMenu.menu.set()

        else:
            await message.reply("Неправильный выбор! Пожалуйста, выберите из главного меню.")
