import time
import random
import re
import os
import subprocess
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ========== НАСТРОЙКИ ==========
CONFIG = {
    "375": ("belarus.txt", "02.jpg"),
    "79":  ("russia.txt", "01.jpg"),
    "77":  ("kazakh.txt", "03.jpg"),
}
DEFAULT_CONFIG = ("russia.txt", "01.jpg")

RECIPIENTS_FILE = "recipients.txt"
SENT_LOG_FILE = "sent.txt"
MIN_DELAY_SEC = 45
MAX_DELAY_SEC = 90
MAX_SEND_COUNT = 5


def read_file_text(filepath):
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
                print(f"Ошибка: {line} - пропускаем")
                continue
            fio, link = parts
            name_parts = fio.split()
            if len(name_parts) < 2:
                print(f"Не удалось извлечь имя из: {fio}")
                continue
            first_name = name_parts[1]
            match = re.search(r'wa\.me/(\d+)', link)
            if not match:
                print(f"Не удалось извлечь номер из ссылки: {link}")
                continue
            phone = match.group(1)
            recipients.append({'name': first_name, 'phone': phone})
    return recipients


def get_config_for_phone(phone):
    for prefix, cfg in CONFIG.items():
        if phone.startswith(prefix):
            return cfg
    return DEFAULT_CONFIG


def already_sent(phone, sent_log):
    return phone in sent_log


def mark_sent(phone, sent_log, log_file):
    sent_log.add(phone)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{phone}\n")


def copy_image_to_clipboard(image_path):
    abs_path = os.path.abspath(image_path)
    ps_command = f'''
    Add-Type -AssemblyName System.Windows.Forms
    $img = [System.Drawing.Image]::FromFile("{abs_path}")
    $clip = [System.Windows.Forms.Clipboard]::SetImage($img)
    '''
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)


def send_whatsapp_message(driver, phone: str, full_message: str, image_path: str = None):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone}")
        print(f"  Открыт чат с {phone}")
        wait = WebDriverWait(driver, 180)

        # Проверка на незарегистрированный номер
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

        message_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@contenteditable='true' and @role='textbox']")
        ))
        print("  Поле ввода найдено.")

        # Вставляем текст
        pyperclip.copy(full_message)
        message_box.click()
        time.sleep(0.3)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        print("  Текст вставлен.")
        time.sleep(0.5)

        # Вставляем изображение (если есть)
        if image_path and os.path.exists(image_path):
            copy_image_to_clipboard(image_path)
            print("  Изображение скопировано в буфер обмена.")
            message_box.click()
            time.sleep(0.3)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            print("  Изображение вставлено. Ждём предпросмотр...")
            time.sleep(4)

        # Отправляем сообщение
        try:
            # Основной селектор
            send_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']"))
            )
            send_btn.click()
            print("  Сообщение отправлено через кнопку.")
        except:
            try:
                # Альтернативный селектор (aria-label)
                send_btn = driver.find_element(By.XPATH, "//div[@aria-label='Отправить']")
                send_btn.click()
                print("  Сообщение отправлено через aria-label.")
            except:
                # Запасной вариант: Enter
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                print("  Сообщение отправлено через Enter.")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"  Ошибка: {e}")
        return False


def main():
    templates = {}
    for prefix, (msg_file, _) in CONFIG.items():
        try:
            templates[prefix] = read_file_text(msg_file)
        except Exception as e:
            print(f"Не удалось прочитать {msg_file}: {e}")
            return
    try:
        default_template = read_file_text(DEFAULT_CONFIG[0])
    except:
        default_template = ""

    recipients = parse_recipients(RECIPIENTS_FILE)
    if not recipients:
        print("Нет получателей.")
        return
    print(f"Загружено {len(recipients)} получателей.")

    sent_phones = set()
    if os.path.exists(SENT_LOG_FILE):
        with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
            sent_phones = set(line.strip() for line in f)

    pending = [r for r in recipients if not already_sent(r['phone'], sent_phones)]
    print(f"Из них не отправлено: {len(pending)}")
    if not pending:
        print("Все уже отправлены.")
        return

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/Temp/WhatsAppProfile")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        time.sleep(1)
        print("Начинаем рассылку. При первом запуске отсканируйте QR-код.\n")
        success_count = 0
        for idx, rec in enumerate(pending):
            if MAX_SEND_COUNT and success_count >= MAX_SEND_COUNT:
                print(f"Лимит {MAX_SEND_COUNT} достигнут. Завершаем.")
                break

            name = rec['name']
            phone = rec['phone']
            cfg = get_config_for_phone(phone)
            msg_file, img_file = cfg
            if phone.startswith("375"):
                template = templates.get("375", default_template)
            elif phone.startswith("79"):
                template = templates.get("79", default_template)
            elif phone.startswith("77"):
                template = templates.get("77", default_template)
            else:
                template = default_template

            full_message = f"{name}, здравствуйте 👋\n{template}"
            print(f"\n--- Отправка {idx+1} из {len(pending)} ---")
            print(f"Получатель: {name}, номер: {phone}")
            print(f"Текст: {msg_file}, картинка: {img_file}")

            ok = send_whatsapp_message(driver, phone, full_message, img_file)
            if ok:
                success_count += 1
                mark_sent(phone, sent_phones, SENT_LOG_FILE)
                if idx < len(pending) - 1:
                    delay = random.randint(MIN_DELAY_SEC, MAX_DELAY_SEC)
                    print(f"Пауза {delay} секунд перед следующим...")
                    time.sleep(delay)
            else:
                print(f"Пропускаем {phone}. Продолжаем без паузы.")
        print(f"\nРассылка завершена. Отправлено: {success_count} из {len(pending)}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()


if __name__ == "__main__":
    main()
