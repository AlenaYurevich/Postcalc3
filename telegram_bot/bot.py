from telebot import TeleBot
from django.conf import settings

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


# Все обработчики должны использовать декоратор
@bot.message_handler(commands=['start'])
@admin_required
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать, администратор!")


@bot.message_handler(commands=['stats'])
@admin_required
def handle_stats(message):
    # Ваша логика для админ-команды
    bot.send_message(message.chat.id, "Статистика: ...")


@bot.message_handler(func=lambda m: True)
@admin_required
def handle_all_messages(message):
    bot.send_message(message.chat.id, "Команда не распознана")


@bot.callback_query_handler(func=lambda call: True)
@admin_required
def handle_callback(call):
    if is_admin(call.message):
        bot.answer_callback_query(call.id, "Обработка...")
    else:
        bot.answer_callback_query(call.id, "Доступ запрещен!", show_alert=True)
