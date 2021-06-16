import logging
from os import environ

from aiogram import Bot, Dispatcher
import aiogram

# Logging
logging.basicConfig(filename="bot.log", filemode="a", encoding="utf-8")

API_TOKEN = environ["PEE_BOOKING_BOT_TOKEN"]

# Bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def handle_start(message: aiogram.types.Message):
    keyboard_markup = aiogram.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True
    )
    keyboard_markup.row(aiogram.types.KeyboardButton("Хочу список команд!🙈"))
    await message.reply(
        f"Вечер в хату, @{message.chat.username}.\nЭтот бот поможет вам онлайн "
        "встать в очередь в душ, чтобы все успели пойти под струю мыться, ваши "
        "соседи не орали как Братишка, а комната не превратилась в гаупвахту.\n"
        "А то Арсений Воронин курлыкать начнёт…\nНаберите /help для просмотра"
        "списка команд",
        reply_markup=keyboard_markup,
    )


@dp.message_handler(commands=["help"])
@dp.message_handler(text=["Посмотреть список команд!🙈", "Хочу список команд!🙈"])
async def handle_help(message: aiogram.types.Message):
    keyboard_markup = aiogram.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True
    )
    buttons = (
        "Записаться в душ 🚿",
        "Выйти из очереди🤢",
        "Посмотреть расписание⌚",
        "Посмотреть список команд!🙈",
    )
    keyboard_markup.add(*(aiogram.types.KeyboardButton(text) for text in buttons))
    await message.reply(
        f"Доступны следующие команды:\n"
        "/help - показ этой помощи\n"
        "/sign - записаться в очередь <s>на приём к Арсению Воронину</s> помыться\n"
        "/delete - выписаться из очереди под струю (только это, ты всё равно помойся, окей?)\n"
        "/timetable - посмотреть расписание душа",
        reply_markup=keyboard_markup,
        parse_mode=aiogram.types.ParseMode.HTML,
    )


@dp.message_handler(commands=["/timetable"])
def handle_timetable(message):
    ...
    # TODO: shower timetable


if __name__ == "__main__":
    aiogram.utils.executor.start_polling(dp)
