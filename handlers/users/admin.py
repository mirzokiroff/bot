from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.languages import uz
from loader import dp, db
from states.personalData import Admin, MainMenu


@dp.message_handler(commands="admin", state='*')
async def admin_handler(message: types.Message):
    if message.from_user.id == 5467465403:
        await message.answer(f"Assalomu alaykum {message.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️")
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

        await message.reply("Iltimos quyidagi kurslardan birini tanlang! va tanlagan kursingizga oid videoni yuboring!",
                            reply_markup=types.ReplyKeyboardMarkup(
                                keyboard=courses_keyboard,
                                resize_keyboard=True, row_width=True
                            ))
        await Admin.video.set()

    else:
        await message.answer("Siz admin emassiz ❌")


@dp.message_handler(state=Admin.video)
async def send_course_video(message: types.Message):
    selected_course_name = message.text

    selected_course = await db.select_course(course_name=selected_course_name)

    if selected_course:
        await message.answer("Video yuborishingiz mumkun 🎬", reply_markup=types.ReplyKeyboardRemove())
        await Admin.add_video.set()
    elif selected_course_name == uz.bosh_menu:
        await message.reply(uz.bosh_menu, reply_markup=types.ReplyKeyboardMarkup(  # noqa
            keyboard=[
                [types.KeyboardButton(text=uz.kurslar), types.KeyboardButton(text=uz.markaz_haqida)],
                [types.KeyboardButton(text=uz.manzil), types.KeyboardButton(text=uz.biz_bn_aloqa)],
            ],
            resize_keyboard=True
        ))
        await MainMenu.menu.set()
    else:
        await message.answer("Kechirasiz, kurs topilmadi. Iltimos, boshqa kurs tanlang.")


@dp.message_handler(state=Admin.add_video, content_types=types.ContentType.VIDEO)
async def handle_video(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['file_id'] = msg.video.file_id
        await msg.answer(f"Videoning file_id si: {data['file_id']}")
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

        await msg.reply(
            "Istasangiz yana kerakli kursni tanlab video yuborishingiz mumkun"
            "\n\nESLATMA: Animation(gif) emas Video yuboring",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=courses_keyboard,
                resize_keyboard=True, row_width=True
            ))
        await Admin.video.set()
    except:
        await msg.answer("Iltimos videoni yuboring!")
