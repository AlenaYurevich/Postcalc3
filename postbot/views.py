import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import async_to_sync
from .access import TF_token
import logging


logger = logging.getLogger(__name__)


TOKEN = TF_token
application = Application.builder().token(TOKEN).build()


# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("Привет! Я твой бот.")


# Обработка текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(f"Вы сказали: {update.message.text}")


# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(json_data, application.bot)
            async_to_sync(application.update_queue.put)(update)
            return HttpResponse(status=200)  # Явно возвращаем успешный ответ
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return HttpResponse(status=500)
    return HttpResponse("Hello from Telegram Bot!", status=200)
