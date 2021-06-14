import telebot, requests

token_file = open("token", "r")
token = token_file.readline().replace("\n", "")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def handle_start(message):
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add("Хочу список команд!🙈")
	msg = bot.reply_to(message, f'Вечер в хату, @{message.from_user.username}.\nЭтот бот поможет вам онлайн встать в очередь в душ, чтобы все успели пойти под струю мыться, ваши соседи не орали как Братишка, а комната не превратилась в гаупвахту.\nА то Арсений Воронин курлыкать начнёт…\nНаберите /help для просмотра списка команд', reply_markup=markup)
	bot.register_next_step_handler(msg, process_step)

@bot.message_handler(commands=["help"])
def handle_help(message):
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add("Записаться в душ 🚿", "Выйти из очереди🤢", "Посмотреть расписание⌚",
	           "Посмотреть список команд!🙈")
	msg = bot.reply_to(message, f'Доступны следующие команды:\n/help - показ этой помощи\n/sign - записаться в очередь под струю\n/delete - выписаться из очереди под струю (только это, ты всё равно помойся, окей?)\n/timetable - посмотреть расписание душа', reply_markup=markup)
	bot.register_next_step_handler(msg, process_step)

@bot.message_handler(commands=["/timetable"])
def handle_timetable(message):
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add("Записаться в душ 🚿", "Выйти из очереди🤢", "Посмотреть расписание⌚",
	           "Посмотреть список команд!🙈")
	msg = bot.reply_to(message, f'', reply_markup=markup)
	bot.register_next_step_handler(msg, process_step)

def process_step(message):
	if message.text == "Хочу список команд!🙈" or message.text == "Посмотреть список команд!🙈":
		handle_help(message)

bot.polling(none_stop=True)
