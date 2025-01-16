import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler
from access import My_token


# Ваша функция, которая будет получать и проверять страницу
def check_page():
    url = "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/fiz"
    response = requests.get(url)
    response.raise_for_status()  # Проверяем на успешность запроса

    soup = BeautifulSoup(response.text, 'html.parser')
    # Ищем элемент по тексту
    element = soup.find_all(string="Прейскурант РБ с 01.01.2025.pdf")

    return "Прейскурант найден." if element else "Прейскурант не найден."


result = check_page()

# # Функция-обработчик команды /start
# async def start(update: Update):
#     await update.message.reply_text('Привет! Используйте команду /check для проверки наличия прейскуранта.')
#
#
# # Функция-обработчик команды /check
# async def check(update: Update):
#     result = check_page()
#     await update.message.reply_text(result)
#
#
# async def main():
#     # Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен бота
#     application = Application.builder().token(My_token).build()
#
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("check", check))
#
#     await application.run_polling()
#
#     # Запуск бота
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
