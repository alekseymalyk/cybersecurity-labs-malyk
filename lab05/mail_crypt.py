# ЛР5 Захищена електронна пошта
# простий шифратор листів: ключ з особистих даних, симетричне шифрування XOR + SHA-256
# Малик Олексій, 6.04.122.010.23.1

import hashlib
import base64
import os

# мої дані, з них роблю ключ
my_email = "oleksii.malyk@hneu.net"
my_name = "OleksiiMalyk"
my_year = "2005"
friend_email = "odnogrupnyk@hneu.net"


# ключ: SHA-256 від пошти + імені + року народження
def make_key(email, name, year):
    text = email + name + year
    return hashlib.sha256(text.encode("utf-8")).digest()


# потік байтів для шифрування: SHA-256(ключ + сіль + номер блоку), блок за блоком
def make_stream(key, salt, length):
    stream = b""
    block = 0
    while len(stream) < length:
        stream = stream + hashlib.sha256(key + salt + str(block).encode()).digest()
        block = block + 1
    return stream


# шифрування: кожен байт тексту XOR з байтом потоку, результат у base64
# сіль (8 випадкових байтів) кладу на початок, щоб однакові листи шифрувались по-різному
def encrypt(text, key):
    data = text.encode("utf-8")
    salt = os.urandom(8)
    stream = make_stream(key, salt, len(data))
    result = []
    for i in range(len(data)):
        result.append(data[i] ^ stream[i])
    return base64.b64encode(salt + bytes(result)).decode()


# розшифрування: відрізаю сіль, те саме XOR ще раз повертає текст
def decrypt(code, key):
    all_data = base64.b64decode(code)
    salt = all_data[0:8]
    data = all_data[8:]
    stream = make_stream(key, salt, len(data))
    result = []
    for i in range(len(data)):
        result.append(data[i] ^ stream[i])
    try:
        return bytes(result).decode("utf-8")
    except UnicodeDecodeError:
        return "(не вдалося прочитати: неправильний ключ)"


# зберігаю лист як файл: заголовки відкриті, текст зашифрований
def save_letter(path, sender, to, subject, code):
    f = open(path, "w", encoding="utf-8")
    f.write("From: " + sender + "\n")
    f.write("To: " + to + "\n")
    f.write("Subject: " + subject + "\n")
    f.write("\n")
    f.write(code + "\n")
    f.close()


def read_letter_body(path):
    f = open(path, encoding="utf-8")
    lines = f.read().split("\n")
    f.close()
    return lines[4]   # перші 4 рядки це заголовки і порожній рядок


print("=== ЛР5: шифратор листів ===")
text = input("Мій лист (Enter = приклад): ")
if text == "":
    text = "Привіт! Здаємо ЛР5 в п'ятницю о 10:40, аудиторія 412."

print()
print("--- Ключ ---")
key = make_key(my_email, my_name, my_year)
print("Дані:", my_email + my_name + my_year)
print("Ключ SHA-256:", key.hex())
print("Цей ключ я передаю одногрупнику через PGP, а не відкритим листом")

print()
print("--- Я шифрую і відправляю ---")
code = encrypt(text, key)
print("Текст:     ", text)
print("Шифротекст:", code)
os.makedirs("mail", exist_ok=True)
save_letter("mail/letter1.txt", my_email, friend_email, "ЛР5", code)
print("Лист збережено: mail/letter1.txt")

print()
print("--- Одногрупник отримує і розшифровує тим самим ключем ---")
got = read_letter_body("mail/letter1.txt")
print("Розшифровано:", decrypt(got, key))
print("Той самий текст ще раз:", encrypt(text, key))
print("Шифротекст інший, бо сіль кожен раз нова")

print()
print("--- Одногрупник відповідає ---")
answer = "Ок, буду. Візьми з собою ключ GPG на флешці."
code2 = encrypt(answer, key)
save_letter("mail/letter2.txt", friend_email, my_email, "Re: ЛР5", code2)
print("Шифротекст:", code2)
print("Я розшифровую:", decrypt(code2, key))

print()
print("--- Хтось перехопив лист і пробує вгадати ключ ---")
wrong_key = make_key(my_email, my_name, "2004")
print("Пробує рік 2004 замість 2005:")
print("Результат:", decrypt(got, wrong_key))

print()
print("--- Що бачить пошта ---")
f = open("mail/letter1.txt", encoding="utf-8")
print(f.read())
f.close()
print("Від кого, кому і тема видно, текст ні")
