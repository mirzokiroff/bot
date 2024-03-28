from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("Biror muammo, savol yoki fikr paydo bo'lgan bo'lsa, Admin yoki Bot Dasturchisiga murojaat qilishingiz mumkun"
            "\nAdmin: @extra_markazi\nBot Dasturchisi: @mirzokirov1"
            "\n\n\nЕсли у вас есть какие-либо проблемы, вопросы или предложения, вы можете связаться с администратором или разработчиком бота."
            "\nАдмин: @extra_markazi\nРазработчик бота: @mirzokirov1")

    await message.answer(text)
