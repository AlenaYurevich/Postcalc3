from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class PostbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postbot'

    def ready(self):
        # Импортируем внутри метода, чтобы избежать циклических импортов
        from .views import application

        try:
            logger.info("Попытка установки вебхука...")
            url = "https://posttarif.by/telegram/webhook/"

            # Проверка доступности токена
            if not application.bot.token:
                logger.error("Токен бота не обнаружен!")
                return

            result = application.bot.set_webhook(url)
            logger.info(f"Вебхук установлен: {result}")
            logger.info(f"Информация о вебхуке: {application.bot.get_webhook_info()}")

        except Exception as e:
            logger.error(f"Критическая ошибка: {str(e)}", exc_info=True)
