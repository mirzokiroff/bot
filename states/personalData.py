from aiogram.dispatcher.filters.state import StatesGroup, State


class PersonalData(StatesGroup):
    fullname = State()
    phone_number = State()
    phone_number_for_call = State()
    activity = State()
    confirmm_data = State()
    confirm_data = State()
    start = State()


class Language(StatesGroup):
    languages = State()
    select_language = State()


class MainMenu(StatesGroup):
    main_menu = State()
    course_selection = State()
    menu = State()


class Courses(StatesGroup):
    course_menu = State()
    course_type_selection = State()
    course_selection = State()
    course_video = State()
    english_video = State()
    russian_video = State()


class Register_Course(StatesGroup):
    course_type = State()


class Education(StatesGroup):
    video_text = State()
    hisobot = State()
    button = State()


class contact_us(StatesGroup):
    contact_us = State()


class Admin(StatesGroup):
    video = State()
    add_video = State()
    reklama = State()
