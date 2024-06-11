from cryptography.fernet import Fernet
from key_manager import load_key, load_user_credentials
from datetime import datetime

key = load_key()

def get_user_credentials():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password

def verify_user(username, password):
    stored_username, stored_password = load_user_credentials()
    return username == stored_username and password == stored_password

def decrypt_log(encrypted_content):
    f = Fernet(key)
    decrypted_content = f.decrypt(encrypted_content)
    return decrypted_content.decode('utf-8')

def format_log_content(log_content):
    formatted_content = ""
    for line in log_content.splitlines():
        if line.strip():
            try:
                log_entry, timestamp = line.rsplit('[', 1)
                timestamp = timestamp.rstrip(']')
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                formatted_content += f"{log_entry.strip()} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            except ValueError:
                formatted_content += line + '\n'
    return formatted_content

def print_in_chunks(content, chunk_size=10):
    buffer = ""
    for char in content:
        buffer += char
        if len(buffer) >= chunk_size:
            print(buffer, end='', flush=True)
            buffer = ""
    if buffer:
        print(buffer, end='', flush=True)

def main():
    username, password = get_user_credentials()
    if verify_user(username, password):
        with open("e_log.txt", "rb") as file:
            encrypted_contents = file.read().split(b'|')
        decrypted_contents = ""
        for encrypted_content in encrypted_contents:
            if encrypted_content:
                decrypted_contents += decrypt_log(encrypted_content)
        formatted_contents = format_log_content(decrypted_contents)
        print("Decryption successful. Log content:")
        print_in_chunks(formatted_contents)

        decrypted_log_file = "decrypted_log.txt"
        with open(decrypted_log_file, "w", encoding="utf-8") as file:
            file.write(formatted_contents)
        print(f"\nDecrypted log content saved to {decrypted_log_file}")
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    main()