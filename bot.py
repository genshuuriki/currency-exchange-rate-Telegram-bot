import telebot
from telebot import types
from main import get_exchange_rates, get_exchange_rates_for_date, format_rates, search_currency

API_KEY = 'your_api_key_here'
bot = telebot.TeleBot(API_KEY)

# Словарь для хранения состояния пользователей
user_states = {}

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    # Создание клавиатуры с кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = types.KeyboardButton(text="💵 Получить курсы валют")
    button2 = types.KeyboardButton(text="🔍 Найти валюту")
    keyboard.add(button1, button2)

    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id,
                     'Данный бот предоставляет Официальные курсы валют, установленные Центральным банком Российской Федерации.',
                     reply_markup=keyboard)


# Обработка нажатий на кнопки клавиатуры
@bot.message_handler(func=lambda message: message.text == "💵 Получить курсы валют")
def handle_get_rates(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Текущая дата", callback_data="current_date_rates")
    button2 = types.InlineKeyboardButton(text="Конкретная дата", callback_data="specific_date_rates")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберите дату для получения курсов валют:', reply_markup=keyboard)


# Обработка нажатий на кнопки для выбора даты
@bot.callback_query_handler(func=lambda call: call.data in ["current_date_rates", "specific_date_rates"])
def handle_date_selection(call):
    if call.data == "current_date_rates":
        date_text, rates = get_exchange_rates()
    elif call.data == "specific_date_rates":
        user_states[call.message.chat.id] = 'waiting_for_date'
        bot.send_message(call.message.chat.id, 'Введите дату в формате dd.mm.yyyy. Дата не может быть раньше 01.07.1992.\nПример: 31.12.2023')
        return

    if not date_text or not rates:
        bot.send_message(call.message.chat.id, 'Не удалось получить данные. Попробуйте позже.')
        return

    response = format_rates(date_text, rates)
    bot.send_message(call.message.chat.id, response)


# Обработка ввода даты от пользователя
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_date')
def handle_date_input(message: types.Message):
    date_text, rates = get_exchange_rates_for_date(message.text.strip())

    if date_text is None or rates is None:
        bot.send_message(message.chat.id, 'Неверная дата или её формат. Попробуйте снова.')
        return

    response = format_rates(date_text, rates)
    bot.send_message(message.chat.id, response)
    user_states[message.chat.id] = None


# Обработка нажатий на кнопку "Найти валюту"
@bot.message_handler(func=lambda message: message.text == "🔍 Найти валюту")
def handle_find_currency(message: types.Message):
    user_states[message.chat.id] = 'waiting_for_currency_input'
    bot.send_message(message.chat.id, 'Введите буквенный код валюты или её название. Пример: USD или Доллар США.')


# Обработка текстовых сообщений для поиска валюты
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_currency_input')
def handle_currency_input(message: types.Message):
    currency_input = message.text.strip()
    date_text, rates = get_exchange_rates()
    response = search_currency(currency_input, date_text, rates)

    if "не найдена" in response:
        bot.send_message(message.chat.id, 'Валюта не найдена. Попробуйте снова.')
        return

    user_states[message.chat.id] = f'waiting_for_currency_date_{currency_input}'
    bot.send_message(message.chat.id, 'Введите дату в формате dd.mm.yyyy. Дата не может быть раньше 01.07.1992.\nПример: 31.12.2023')


# Обработка текстовых сообщений для поиска валюты на конкретную дату после ввода валюты
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, '').startswith('waiting_for_currency_date_'))
def handle_currency_search_date_specific(message: types.Message):
    currency_input = user_states[message.chat.id].replace('waiting_for_currency_date_', '')
    date_input = message.text.strip()
    date_text, rates = get_exchange_rates_for_date(date_input)

    if date_text is None or rates is None:
        bot.send_message(message.chat.id, 'Неверная дата или её формат. Попробуйте снова.')
        user_states[message.chat.id] = f'waiting_for_currency_date_{currency_input}'
        return

    response = search_currency(currency_input, date_text, rates)

    if "не найдена" in response:
        bot.send_message(message.chat.id, response + ' Попробуйте снова.')
        user_states[message.chat.id] = f'waiting_for_currency_date_{currency_input}'
    else:
        bot.send_message(message.chat.id, response)
        user_states[message.chat.id] = None


bot.polling()
