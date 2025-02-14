import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from .access import TF_token


TOKEN = TF_token
application = Application.builder().token(TOKEN).build()


# Обработка команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я твой бот.")


# Обработка текстовых сообщений
async def echo(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")


# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(json_data, application.bot)
            application.process_update(update)
            return HttpResponse(status=200)  # Явно возвращаем успешный ответ
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
        except Exception as e:
            print(f"Ошибка: {e}")
            return HttpResponse(f"Server Error: {e}", status=500)
    return HttpResponse("Hello from Telegram Bot!", status=200)
