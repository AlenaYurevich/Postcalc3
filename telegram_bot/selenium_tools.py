import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('WDM').setLevel(logging.WARNING)  # Показывать только предупреждения и ошибки


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Путь к chromedriver из .wdm
    driver_path = os.path.join(os.getcwd(), "./virtualenv/postcalc2/3.11/lib/python3.11/site-packages/selenium/webdriver/chrome/webdriver.py")

    try:
        # Пытаемся использовать уже скачанный драйвер
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info(f"Используем существующий драйвер: {driver_path}")
        return driver
    except Exception as e:
        # Если не сработало - качаем заново
        logger.warning(f"Ошибка: {str(e)}, пробуем автоматическую установку...")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )


def check_elements_on_pages(url_xpath_map):
    driver = setup_driver()
    results = []
    try:
        for url, xpath in url_xpath_map.items():
            driver.get(url)
            try:
                wait = WebDriverWait(driver, 10)
                # Получаем элемент и сразу используем его
                element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))

                # Теперь переменная element используется
                results.append(
                    f"✅ {url}\n"
                    f"Найден элемент: {element.tag_name}\n"
                    f"Текст: {element.text[:50]}..."  # Пример использования
                )

            except Exception as e:
                results.append(f"❌ {url}\nОшибка: {str(e)}")
    finally:
        driver.quit()
    return "\n\n".join(results)


def search_text_on_page(url, search_text):
    driver = setup_driver()
    results = []
    try:
        driver.get(url)
        search_text_lower = search_text.lower()
        xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'," \
                f" 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'), '{search_text_lower}')]"

        try:
            wait = WebDriverWait(driver, 15)
            elements = wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))

            if elements:
                results.append(f"Найдено {len(elements)} совпадений:")
                for element in elements[:5]:  # Ограничим вывод
                    results.append(f"- {element.text[:100]}...")
            else:
                results.append("Совпадений не найдено")
        except Exception as e:
            results.append(f"Ошибка поиска: {str(e)}")
    finally:
        driver.quit()
    return "\n".join(results)
