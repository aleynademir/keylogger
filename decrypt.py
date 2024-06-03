from cryptography.fernet import Fernet
from key_manager import load_key, load_user_credentials

# Anahtar yükleme
key = load_key()

# Kullanıcı bilgilerini al ve doğrula
def get_user_credentials():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password

# Kullanıcı bilgilerini kontrol et
def verify_user(username, password):
    return username == "aleyna" and password == "123456"

# Şifre çözme
def decrypt_log(encrypted_content):
    f = Fernet(key)
    decrypted_content = f.decrypt(encrypted_content)
    return decrypted_content.decode('utf-8')

# Kullanıcı bilgilerini al ve log dosyasını deşifre et
def main():
    username, password = get_user_credentials()
    if verify_user(username, password):
        with open("e_log.txt", "rb") as file:
            encrypted_contents = file.read().split(b'|')  # Ayırıcıyı kullanarak şifrelenmiş blokları ayırıyoruz
        decrypted_contents = ""
        for encrypted_content in encrypted_contents:
            if encrypted_content:  # Boş olmayan içerikleri çöz
                decrypted_contents += decrypt_log(encrypted_content)
        print("Decryption successful. Log content:")
        print(decrypted_contents)
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    main()
