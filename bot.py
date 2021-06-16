import logging
from os import environ

from aiogram import Bot, Dispatcher
import aiogram
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from bot_backend import UserBackend

# Logging
logging.basicConfig(filename="bot.log", filemode="a", encoding="utf-8")

# Config
API_TOKEN = environ["PEE_BOOKING_BOT_TOKEN"]
SERVER = "http://0.0.0.0:8080"
FLOORS = ["1", "2", "3", "4"]

# Bot
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class reg(StatesGroup):
    gender = aiogram.dispatcher.filters.state.State()
    floor = aiogram.dispatcher.filters.state.State()


@dp.message_handler(commands=["start"])
async def handle_start(message: aiogram.types.Message):
    UserExists = backend.check_user(username=message.chat.username)
    if not UserExists:
        keyboard_markup = aiogram.types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True
        )
        keyboard_markup.row(aiogram.types.KeyboardButton("Зарегистрироваться"))
        await message.reply(
            f"Нужно зарегистрироваться.\n"
            "Нажимая кнопку зарегистрироваться вы даёте своё согласие на обработку "
            "персональных данных согласно 152-ФЗ от 27.07.2006. И да, если вам нет 14, то давать это согласие "
            "вы типа не можете, так что пипи тоже сделать не получится. ¯​\_(ツ)_/¯",
            reply_markup=keyboard_markup,
        )
        return
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


@dp.message_handler(text="Зарегистрироваться", state="*")
async def service_sign_up(message: aiogram.types.Message):
    keyboard_markup = aiogram.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True
    )
    keyboard_markup.row(aiogram.types.KeyboardButton("М"))
    keyboard_markup.row(aiogram.types.KeyboardButton("Ж"))
    await message.reply(
        f"Пол?",
        reply_markup=keyboard_markup,
    )
    await reg.next()


@dp.message_handler(text=["М", "Ж"], state=reg.gender)
async def service_sign_up(
    message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext
):
    await state.update_data(gender=message.text)
    keyboard_markup = aiogram.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True
    )
    for floor in FLOORS:
        keyboard_markup.row(aiogram.types.KeyboardButton(floor))
    await message.reply(
        f"Этаж?",
        reply_markup=keyboard_markup,
    )
    await reg.next()


@dp.message_handler(text=FLOORS, state=reg.floor)
async def service_sign_up(
    message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext
):
    await state.update_data(floor=message.text)
    async with state.proxy() as data:
        if backend.create_user(
            username=message.chat.username, user_id=message.from_user.id, sex=data["gender"], floor=data["floor"]
        ):
            await message.reply("Вы успешно зарегистрировались. /help")
        else:
            await message.reply(
                "Что-то пошло не так. Срочно пишите админам (контакты в описании бота)!"
            )
    await state.finish()


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
@dp.message_handler(text="Посмотреть расписание⌚")
async def shower_timetable(message: aiogram.types.Message):
    ...
    # TODO: shower timetable


@dp.message_handler(commands=["/sign"])
@dp.message_handler(text="Записаться в душ 🚿")
async def make_an_appointement(message: aiogram.types.Message):
    ...
    # TODO: shower sign up


@dp.message_handler(commands=["/delete"])
@dp.message_handler(text="Выйти из очереди🤢")
async def delete_an_appointement(message: aiogram.types.Message):
    ...
    # TODO: shower unsign up


@dp.message_handler()
async def other(message: aiogram.types.Message):
    await message.reply("Не знаю такую команду. Хочешь в душ? Пиши /help")


if __name__ == "__main__":
    backend = UserBackend(SERVER)
    aiogram.utils.executor.start_polling(dp)
