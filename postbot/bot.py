from telebot import TeleBot, types
from django.conf import settings
from postbot.selenium_tools import check_elements_on_pages, search_text_on_page  # postbot!!!!
from threading import Thread

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


def is_admin(message):
    admin_id = getattr(settings, 'TELEGRAM_ADMIN_ID', None)
    if not admin_id:
        raise ValueError("TELEGRAM_ADMIN_ID not set in settings")
    return message.from_user.id == admin_id


def admin_required(func):
    def wrapped(message, *args, **kwargs):
        if not is_admin(message):
            bot.reply_to(message, "🔒 Бот доступен только администратору")
            return
        return func(message, *args, **kwargs)

    return wrapped


def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📰 Новости", "💰 Прейскуранты")
    return keyboard


# Все обработчики должны использовать декоратор
@bot.message_handler(commands=['start'])
@admin_required  # Используем декоратор из предыдущего ответа
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Выберите действие:",
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(commands=['menu'])
@admin_required
def show_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Проверить новости", callback_data='news'),
        types.InlineKeyboardButton("Проверить прейскуранты", callback_data='pricelist')
    )
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
@admin_required
def handle_callback(call):
    if call.data == 'news':
        handle_news(call.message)
    elif call.data == 'pricelist':
        handle_pricelist(call.message)


@bot.message_handler(func=lambda m: m.text == "📰 Новости")
@admin_required
def handle_news(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        result = search_text_on_page("https://blog.belpost.by/", "тариф")
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")


def async_task(func, message, *args):
    def wrapper():
        try:
            result = func(*args)
            bot.send_message(message.chat.id, result)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

    Thread(target=wrapper).start()


@bot.message_handler(func=lambda m: m.text == "💰 Прейскуранты")
@admin_required
def handle_pricelist(message):
    bot.send_message(message.chat.id, "Начинаю проверку прейскурантов...")
    url_xpath_map = {
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/fiz":
            "//a[span[text()='Прейскурант РБ  с 01.03.2025 .pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Tarifynauslugipochtovoysv0":
            "//a[span[text()='Прейскурант РБ  с 01.03.2025 .pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/vnutrennyayauskorennayapo0":
            "//a[span[text()='Прейскурант экспресс посылки с 01.03.2025 .pdf']]",
        "https://www.belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/vnutrennyayauskorennayapo1":
            "//a[span[text()='Прейскурант экспресс посылки  с 01.03.2025 .pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/mezhdunarodnyyepochtovyye1":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД физ лица с 01.01.2025.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/mezhdunarodnyyepochtovyye0":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД юр лица с 01.01.2025.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/Mezhdunarodnyyeposylkidly":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД  посылки физ лица с 01.01.2025).pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Mezhdunarodnyyeposylkidly0":
            "//a[span[text()='2 ПРЕЙСКУРАНТ МЕЖД  посылки с 01.01.2025.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/Mezhdunarodnayauskorennay":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД EMS  ФИЗ ЛИЦА с 01.01.2025).pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Mezhdunarodnayauskorennay0":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД EMS  юр лица с 01.01.2025).pdf']]",
    }
    async_task(check_elements_on_pages, message, url_xpath_map)


@bot.callback_query_handler(func=lambda call: True)
@admin_required
def handle_callback(call):
    if is_admin(call.message):
        bot.answer_callback_query(call.id, "Обработка...")
    else:
        bot.answer_callback_query(call.id, "Доступ запрещен!", show_alert=True)
