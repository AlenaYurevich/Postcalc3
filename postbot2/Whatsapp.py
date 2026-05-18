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
    "375": ("belarus.txt", "02.jpg"),   # Беларусь
    "79":  ("russia.txt", "01.jpg"),    # Россия
    "77":  ("kazakh.txt", "03.jpg"),    # Казахстан
    "996": ("russia.txt", "01.jpg"),    # Киргизия (если нужна)
}
DEFAULT_CONFIG = ("russia.txt", "01.jpg")

RECIPIENTS_FILE = "recipients.txt"
SENT_LOG_FILE = "sent.txt"
FAILED_LOG_FILE = "failed.txt"          # новый файл для неудачных отправок
MIN_DELAY_SEC = 45
MAX_DELAY_SEC = 90
MAX_SEND_COUNT = 7

# ========== ФУНКЦИИ ==========


def read_file_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def extract_phone_number(text):
    """Извлекает номер телефона из строки (ищет цифры, возможно с +) и возвращает только цифры."""
    # Ищем последовательность цифр длиной от 10 до 15 (с возможным + в начале)
    match = re.search(r'\+?(\d{10,15})', text)
    if match:
        return match.group(1)  # возвращаем только цифры
    return None


def parse_recipients(filepath):
    recipients = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 1. Пробуем найти ссылку wa.me/...
            wa_match = re.search(r'wa\.me/(\d+)', line)
            if wa_match:
                phone = wa_match.group(1)
                # ФИО — всё до ссылки
                fio_part = line[:line.find('https://')].strip()
                name_parts = fio_part.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[1]  # второе слово — имя
                elif len(name_parts) == 1:
                    first_name = name_parts[0]
                else:
                    first_name = "Клиент"
                recipients.append({'name': first_name, 'phone': phone, 'raw': line})
                continue
            # 2. Если ссылки нет, пробуем извлечь номер из конца строки
            phone = extract_phone_number(line)
            if phone:
                # Удаляем номер из строки, оставляем ФИО
                # Заменяем найденный номер (с возможным +) на пустоту
                line_without_phone = re.sub(r'\+?\d{10,15}', '', line).strip()
                # Избавляемся от лишних пробелов
                line_without_phone = re.sub(r'\s+', ' ', line_without_phone).strip()
                name_parts = line_without_phone.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[1]  # второе слово — имя
                elif len(name_parts) == 1:
                    first_name = name_parts[0]
                else:
                    first_name = "Клиент"
                recipients.append({'name': first_name, 'phone': phone, 'raw': line})
            else:
                print(f"Не удалось извлечь номер из строки: {line} — пропускаем")
                # Записываем в failed сразу? Лучше позже, но можно и здесь
                with open(FAILED_LOG_FILE, "a", encoding="utf-8") as f_err:
                    f_err.write(f"Ошибка парсинга: {line}\n")
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


def mark_failed(recipient, reason, log_file):
    """Записывает неудачную отправку в файл."""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{recipient['name']} | {recipient['phone']} | {reason} | {recipient.get('raw', '')}\n")


def copy_image_to_clipboard(image_path):
    abs_path = os.path.abspath(image_path)
    ps_command = f'''
    Add-Type -AssemblyName System.Windows.Forms
    $img = [System.Drawing.Image]::FromFile("{abs_path}")
    $clip = [System.Windows.Forms.Clipboard]::SetImage($img)
    '''
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)


def send_whatsapp_message(driver, recipient, full_message, image_path=None):
    phone = recipient['phone']
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
            mark_failed(recipient, "Номер не зарегистрирован в WhatsApp", FAILED_LOG_FILE)
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
            send_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']"))
            )
            send_btn.click()
            print("  Сообщение отправлено через кнопку.")
        except:
            try:
                send_btn = driver.find_element(By.XPATH, "//div[@aria-label='Отправить']")
                send_btn.click()
                print("  Сообщение отправлено через aria-label.")
            except:
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                print("  Сообщение отправлено через Enter.")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"  Ошибка: {e}")
        mark_failed(recipient, f"Исключение: {str(e)[:100]}", FAILED_LOG_FILE)
        return False


def main():
    # Загружаем шаблоны текстов для всех префиксов
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
            # Выбираем шаблон в зависимости от префикса
            if phone.startswith("375"):
                template = templates.get("375", default_template)
            elif phone.startswith("79"):
                template = templates.get("79", default_template)
            elif phone.startswith("77"):
                template = templates.get("77", default_template)
            elif phone.startswith("996"):
                template = templates.get("996", default_template)
            else:
                template = default_template

            full_message = f"{name}, здравствуйте 👋\n{template}"
            print(f"\n--- Отправка {idx+1} из {len(pending)} ---")
            print(f"Получатель: {name}, номер: {phone}")
            print(f"Текст: {msg_file}, картинка: {img_file}")

            ok = send_whatsapp_message(driver, rec, full_message, img_file)
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
        print(f"Неудачные отправки записаны в {FAILED_LOG_FILE}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()


if __name__ == "__main__":
    main()
