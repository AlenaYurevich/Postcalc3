import time
import random
import re
import os
import pyperclip
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ========== НАСТРОЙКИ ==========
MESSAGE_TEMPLATE_FILE = "message.txt"
IMAGE_PATH = "01.jpg"
RECIPIENTS_FILE = "recipients.txt"

MIN_DELAY_SEC = 45
MAX_DELAY_SEC = 90
MAX_SEND_COUNT = None


# ========== ФУНКЦИИ ==========
def read_template(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def parse_recipients(filepath):
    recipients = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit(' ', 1)
            if len(parts) != 2:
                print(f"Ошибка в строке: {line} - пропускаем")
                continue
            fio, link = parts
            name_parts = fio.split()
            if len(name_parts) < 2:
                print(f"Не удалось извлечь имя из: {fio} - пропускаем")
                continue
            first_name = name_parts[1]
            match = re.search(r'wa\.me/(\d+)', link)
            if not match:
                print(f"Не удалось извлечь номер из ссылки: {link} - пропускаем")
                continue
            phone = match.group(1)
            recipients.append({'name': first_name, 'phone': phone})
    return recipients


def close_file_dialog():
    """Закрывает системное окно выбора файла (нажатием Esc)."""
    pyautogui.press('esc')
    time.sleep(0.3)
    pyautogui.press('esc')   # второй раз для надёжности
    time.sleep(0.3)


def send_whatsapp_message(driver, phone: str, full_message: str, image_path: str = None):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone}")
        print(f"  Открыт чат с {phone}")
        wait = WebDriverWait(driver, 30)

        # Проверяем диалог «Номер не зарегистрирован»
        try:
            error_dialog = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@role='dialog']//div[contains(text(), 'не зарегистрирован') or contains(text(), 'not registered')]")
            ))
            print(f"  Номер {phone} не зарегистрирован. Пропускаем.")
            ok_button = driver.find_element(By.XPATH, "//div[@role='dialog']//button")
            ok_button.click()
            time.sleep(1)
            return False
        except:
            pass

        # Ждём поле ввода сообщения
        try:
            message_box = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true' and @role='textbox']")
            ))
        except:
            print(f"  Не удалось найти поле ввода для {phone}.")
            return False

        # Вставляем текст
        pyperclip.copy(full_message)
        message_box.click()
        time.sleep(0.5)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        print("  Текст вставлен.")
        time.sleep(1)

        # Отправка изображения
        if image_path and os.path.exists(image_path):
            # Закрываем возможный висящий диалог перед началом
            close_file_dialog()

            attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus-rounded']")))
            attach_btn.click()
            time.sleep(1.5)
            photo_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Фото и видео']")))
            photo_item.click()
            time.sleep(1.5)

            # Поиск поля загрузки файла с повторными попытками
            file_input = None
            for attempt in range(3):
                try:
                    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                    break
                except:
                    print(f"  Попытка {attempt+1}: поле загрузки не найдено, ждём...")
                    time.sleep(2)
            if file_input is None:
                print("  Не удалось найти поле загрузки. Изображение не отправлено.")
                # Закрываем диалог, если он всё же появился
                close_file_dialog()
                return False

            full_path = os.path.abspath(image_path)
            file_input.send_keys(full_path)
            print("  Файл загружен.")
            time.sleep(3)
            send_img_btn = driver.find_element(By.XPATH, "//div[@aria-label='Отправить']")
            send_img_btn.click()
            print("  Изображение отправлено.")
            time.sleep(5)  # даём время на отправку и закрытие диалога
            # Закрываем системный диалог, если он вдруг появился
            close_file_dialog()
        else:
            # Только текст
            try:
                send_btn = driver.find_element(By.XPATH, "//button[@data-testid='compose-btn-send']")
                send_btn.click()
            except:
                message_box.send_keys(Keys.ENTER)
            print("  Текст отправлен.")
            time.sleep(2)

        return True
    except Exception as e:
        print(f"  Ошибка при отправке {phone}: {e}")
        # Пытаемся закрыть любой диалог
        try:
            ok_btn = driver.find_element(By.XPATH, "//div[@role='dialog']//button")
            ok_btn.click()
        except:
            pass
        close_file_dialog()
        return False


def main():
    try:
        template = read_template(MESSAGE_TEMPLATE_FILE)
    except Exception as e:
        print(f"Ошибка чтения файла шаблона: {e}")
        return

    recipients = parse_recipients(RECIPIENTS_FILE)
    if not recipients:
        print("Нет получателей для рассылки.")
        return

    print(f"Загружено {len(recipients)} получателей.")

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/Temp/WhatsAppProfile")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        time.sleep(1)
        print("Начинаем рассылку. При первом открытии чата отсканируйте QR-код, если потребуется.")

        success_count = 0
        for idx, rec in enumerate(recipients):
            if MAX_SEND_COUNT and success_count >= MAX_SEND_COUNT:
                print(f"Достигнут лимит отправок ({MAX_SEND_COUNT}). Завершаем.")
                break

            name = rec['name']
            phone = rec['phone']
            full_message = f"{name}, здравствуйте 👋\n{template}"

            print(f"\n--- Отправка {idx+1} из {len(recipients)} ---")
            print(f"Получатель: {name}, номер: {phone}")

            ok = send_whatsapp_message(driver, phone, full_message, IMAGE_PATH)
            if ok:
                success_count += 1
                if idx < len(recipients) - 1:
                    delay = random.randint(MIN_DELAY_SEC, MAX_DELAY_SEC)
                    print(f"Пауза {delay} секунд перед следующим сообщением...")
                    time.sleep(delay)
            else:
                print(f"Пропускаем {phone} из-за ошибки. Продолжаем без паузы.")

        print(f"\nРассылка завершена. Отправлено успешно: {success_count} из {len(recipients)}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()


if __name__ == "__main__":
    main()