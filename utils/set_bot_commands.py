from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("language", "Til tanlash"),
            types.BotCommand("admin", "Faqat Admin uchun"),
        ]
    )
