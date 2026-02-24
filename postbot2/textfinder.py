from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('WDM').setLevel(logging.WARNING)  # Показывать только предупреждения и ошибки


def setup_driver():
    # Настройки для запуска браузера в фоновом режиме
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def check_elements_on_pages(url_xpath_map):
    driver = setup_driver()
    try:
        for url, xpath in url_xpath_map.items():
            driver.get(url)
            try:
                # Явное ожидание элемента
                wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд
                element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))

                if element:
                    logger.info(f"Элемент найден на странице {url}")
                else:
                    logger.warning(f"Элемент не найден на странице {url}.")
            except Exception as e:
                logger.error(f"Ошибка на странице {url}: {e}")
    finally:
        driver.quit()


def search_text_on_page(url, search_text):
    driver = setup_driver()
    try:
        driver.get(url)
        # Преобразуем искомый текст в нижний регистр
        search_text_lower = search_text.lower()

        # Ожидание: находим все элементы с текстом без учёта регистра
        wait = WebDriverWait(driver, 15)  # Ожидание до 10 секунд
        try:
            # Используем XPath с translate для нечувствительного поиска
            xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'," \
                    f" 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'), '{search_text_lower}')]"
            elements = wait.until(
                ec.presence_of_all_elements_located((By.XPATH, xpath))
            )

            if elements:
                logger.info(f'Текст "{search_text}" найден в {len(elements)} элементах:')
                for i, element in enumerate(elements, 1):
                    logger.info(f'{i}. {element.text}')
            else:
                logger.warning(f'Текст "{search_text}" не найден на странице.')
        except Exception as e:
            logger.error(f'Ошибка при поиске текста "{search_text}": {e}')
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы {url}: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    # Словарь URL-адресов и соответствующих XPath
    url_xpath_map = {
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/fiz":
            "//a[span[text()='Прейскурант физ лица  с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Tarifynauslugipochtovoysv0":
            "//a[span[text()='Прейскурант   с 01.01.2026 .pdf']]",
        "https://www.belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/oplachennaja-peresylka":
            "//span[em[text()='В действии с 01.01.2026']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/vnutrennyayauskorennayapo0":
            "//a[span[text()='Прейскурант экспресс посылка с 01.01.2026.pdf']]",
        "https://www.belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/vnutrennyayauskorennayapo1":
            "//a[span[text()='Прейскурант экспресс посылки  с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/mezhdunarodnyyepochtovyye1":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД  с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/mezhdunarodnyyepochtovyye0":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/Tarify-na-peresylku-mezdu":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД  МП с 01.1.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Tarify-na-peresylku-mezdu0":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД. МП с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/Mezhdunarodnyyeposylkidly":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД посылки с 01.1.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Mezhdunarodnyyeposylkidly0":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД посылки с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/Mezhdunarodnayauskorennay":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД EMS  с 01.01.2026.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Mezhdunarodnayauskorennay0":
            "//a[span[text()='ПРЕЙСКУРАНТ МЕЖД EMS с 01.01.2026.pdf']]",
    }

    check_elements_on_pages(url_xpath_map)
    # Поиск текста "тариф" на странице блога
    search_text_on_page("https://blog.belpost.by/", "тариф")
    search_text_on_page("https://blog.belpost.by/", "об изменении")
