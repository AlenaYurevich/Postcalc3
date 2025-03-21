import telebot
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .bot import bot


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    return HttpResponse('')
