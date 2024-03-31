import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.languages import uz
from loader import dp, db, bot
from states.personalData import Admin, MainMenu
from environs import Env  # noqa

env = Env()
env.read_env()

ADMIN_IDS = env.list("ADMINS")


@dp.message_handler(commands="admin", state='*')
async def admin_handler(message: types.Message):
    is_admin = False
    for admin in ADMIN_IDS:
        if message.from_user.id == int(admin):
            is_admin = True
            break

    if is_admin:
        await message.answer(f"Assalomu alaykum {message.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️",
                             reply_markup=types.ReplyKeyboardRemove())
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
        courses_keyboard.append([types.KeyboardButton(text="Reklama")])

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
    elif selected_course_name == "Reklama":
        await message.reply("Tayyor Reklamani Jo'nating!", reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Bekor qilish")]], resize_keyboard=True))
        await Admin.reklama.set()
    else:
        await message.answer("Kechirasiz, kurs topilmadi. Iltimos, boshqa kurs tanlang.")


@dp.message_handler(state=Admin.add_video, content_types=types.ContentType.VIDEO)
async def handle_video(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['file_id'] = msg.video.file_id
        await msg.answer(f"Videoning file_id si:")
        await msg.answer(f"{data['file_id']}")
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
        courses_keyboard.append([types.KeyboardButton(text="Reklama")])

        await msg.reply(
            "Istasangiz yana kerakli kursni tanlab video yuborishingiz mumkun"
            "\n\nESLATMA: Animation(gif) emas Video yuboring",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=courses_keyboard,
                resize_keyboard=True, row_width=True
            ))
        await Admin.video.set()
    except:  # noqa
        await msg.answer("Iltimos videoni yuboring!")


@dp.message_handler(state=Admin.reklama, content_types=types.ContentType.ANY)
async def handle_reklama(msg: types.Message, state: FSMContext):
    all_users = await db.select_all_users()
    if msg.text == "Bekor qilish":
        await msg.answer("Bekor qilindi")
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
        courses_keyboard.append([types.KeyboardButton(text="Reklama")])

        await msg.reply(
            "Istasangiz yana Istalgan Reklamani yuborishingiz mumkun\n\n"
            "Eslatma!!! Siz nima yuborsangiz foydalanuvchilarga ham yuboriladi",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=courses_keyboard,
                resize_keyboard=True, row_width=True
            ))
        await Admin.video.set()
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅")
        try:
            summa = 0
            blocked_users = []
            for user in all_users:
                user_id = user['id']
                if int(user['telegram_id']) != 5467465403:
                    try:
                        await msg.copy_to(int(user['telegram_id']), caption=msg.caption,
                                          caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
                    except aiogram.exceptions.ChatNotFound as e:
                        print(f"User with ID {user_id} User with Username "
                              f"{user['full_name']} not found or has blocked the bot. {e}")
                        summa += 1
                        blocked_users.append(user['full_name'])
            await bot.send_message(ADMIN_IDS[0], text=f"Botni bloklagan yoki topilmagan Userlar soni: {summa}"
                                                      f"\n\nBotni bloklagan yoki topilmagan Userlar: {blocked_users}")
            await state.finish()
            await msg.answer("Reklama barcha foydalanuvchilarga muvaffaqiyatli yuborildi!")
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
            courses_keyboard.append([types.KeyboardButton(text="Reklama")])

            await msg.reply(
                "Istasangiz yana Istalgan Reklamani yuborishingiz mumkun\n\n"
                "Eslatma!!! Siz nima yuborsangiz foydalanuvchilarga ham yuboriladi",
                reply_markup=types.ReplyKeyboardMarkup(
                    keyboard=courses_keyboard,
                    resize_keyboard=True, row_width=True
                ))
            await Admin.video.set()
        except Exception as e:
            print(f"Error: {e}")
