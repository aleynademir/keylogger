from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.txt", "wb") as key_file:
        key_file.write(key)

def load_key():
    with open("encryption_key.txt", "rb") as key_file:
        key = key_file.read()
    return key

def load_user_credentials():
    return "aleyna", "123456"

if __name__ == "__main__":
    generate_key()
