from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib


def derive_key_from_password(password):
    # Создание хеша пароля с использованием SHA-256
    return hashlib.sha256(password.encode()).digest()


def encrypt_file(input_file, output_file):
    password = input("Input a password: ")
    # Генерация ключа из пароля
    key = derive_key_from_password(password)

    # Генерация случайного вектора инициализации (IV)
    iv = get_random_bytes(16)

    # Создание объекта шифра AES в режиме CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Чтение содержимого входного файла
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Дополнение (padding) данных до кратного размера блока
    padded_data = pad(plaintext, AES.block_size)

    # Шифрование данных
    ciphertext = cipher.encrypt(padded_data)

    # Запись вектора инициализации и зашифрованных данных в выходной файл
    with open(output_file, 'wb') as f:
        f.write(iv)
        f.write(ciphertext)


def decrypt_file(input_file, output_file):
    password = input("Input a password: ")
    # Генерация ключа из пароля
    key = derive_key_from_password(password)

    # Чтение содержимого входного файла
    with open(input_file, 'rb') as f:
        iv = f.read(16)  # Чтение вектора инициализации
        ciphertext = f.read()

    # Создание объекта шифра AES в режиме CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Дешифрование данных
    padded_data = cipher.decrypt(ciphertext)

    # Удаление дополненных (padded) данных
    plaintext = unpad(padded_data, AES.block_size)

    # Запись дешифрованных данных в выходной файл
    with open(output_file, 'wb') as f:
        f.write(plaintext)
