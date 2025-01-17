from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def check_elements_on_pages(url_xpath_map):
    # Настройки для запуска браузера в фоновом режиме
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        for url, xpath in url_xpath_map.items():
            driver.get(url)
            try:
                # Явное ожидание элемента
                wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                if element:
                    print(f"Элемент найден на странице {url}: {element.get_attribute('href')}")
                else:
                    print(f"Элемент не найден на странице {url}.")
            except Exception as e:
                print(f"Ошибка на странице {url}: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    # Словарь URL-адресов и соответствующих XPath
    url_xpath_map = {
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyfiz/fiz":
            "//a[span[text()='Прейскурант РБ с 01.01.2025.pdf']]",
        "https://belpost.by/Tarify2/TarifyRUPBelpochta/Tarifyyur/Tarifynauslugipochtovoysv0":
            "//a[span[text()='Прейскурант юр. лица с  01.01.2025.pdf']]",

        # Добавьте остальные URL и их XPath
    }

    check_elements_on_pages(url_xpath_map)
