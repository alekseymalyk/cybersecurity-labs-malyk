# ЛР2 Захист особистих повідомлень
# шифр Цезаря і шифр Віженера для українського тексту
# Малик Олексій, 6.04.122.010.23.1

alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"   # 33 букви

# ключі беру зі своїх даних
birth_date = "23.12.2005"
surname = "малик"

# цей текст береться якщо нічого не ввести
my_text = "Зустрінемось біля бібліотеки ХНЕУ о пів на третю"


# ключ для Цезаря: складаю всі цифри дати (2+3+1+2+2+0+0+5 = 15)
def make_caesar_key(date):
    total = 0
    for c in date:
        if c.isdigit():
            total = total + int(c)
    return total


# зсуває одну букву на shift позицій
# якщо це не буква з алфавіту (пробіл, цифра, латиниця) то повертаю як є
def shift_letter(c, shift):
    small = c.lower()
    if small not in alphabet:
        return c
    pos = alphabet.index(small)
    # % щоб після "я" знову почати з "а"
    new_pos = (pos + shift) % len(alphabet)
    letter = alphabet[new_pos]
    if c.isupper():
        letter = letter.upper()
    return letter


def caesar_encrypt(text, shift):
    res = ""
    for c in text:
        res = res + shift_letter(c, shift)
    return res


def caesar_decrypt(text, shift):
    res = ""
    for c in text:
        res = res + shift_letter(c, -shift)
    return res


# Віженер: кожна буква зсувається на номер відповідної букви ключа
# ключ повторюється по колу: м а л и к м а л и к ...
def vigenere_encrypt(text, key):
    res = ""
    i = 0
    for c in text:
        if c.lower() in alphabet:
            shift = alphabet.index(key[i % len(key)])
            res = res + shift_letter(c, shift)
            i = i + 1
        else:
            res = res + c
    return res


# те саме, тільки зсув в іншу сторону
def vigenere_decrypt(text, key):
    res = ""
    i = 0
    for c in text:
        if c.lower() in alphabet:
            shift = alphabet.index(key[i % len(key)])
            res = res + shift_letter(c, -shift)
            i = i + 1
        else:
            res = res + c
    return res


# рахую яка буква зустрічається найчастіше
def most_common_letter(text):
    best = ""
    best_count = 0
    for letter in alphabet:
        count = text.lower().count(letter)
        if count > best_count:
            best_count = count
            best = letter
    return best, best_count


# злом Цезаря: просто пробую всі зсуви і дивлюсь де вийде нормальний текст
def brute_force(text):
    print("Злом шифру Цезаря перебором:")
    for shift in range(1, len(alphabet)):
        print(shift, caesar_decrypt(text, shift))


# ---------- основна частина ----------

print("Шифр Цезаря і шифр Віженера")
text = input("Введіть текст (Enter - мій текст): ")
if text == "":
    text = my_text

caesar_key = make_caesar_key(birth_date)
vigenere_key = surname

caesar_text = caesar_encrypt(text, caesar_key)
vigenere_text = vigenere_encrypt(text, vigenere_key)

print()
print("Відкритий текст:", text)
print()
print("Цезар, зсув", caesar_key, "(сума цифр дати", birth_date + ")")
print("Зашифровано:  ", caesar_text)
print("Розшифровано: ", caesar_decrypt(caesar_text, caesar_key))
print()
print("Віженер, ключ", vigenere_key, "(прізвище)")
print("Зашифровано:  ", vigenere_text)
print("Розшифровано: ", vigenere_decrypt(vigenere_text, vigenere_key))

# порівняння двох шифрів
print()
print("Порівняння:")
print("Довжина тексту:", len(text), "| Цезар:", len(caesar_text), "| Віженер:", len(vigenere_text))
# у Цезаря 32 варіанти зсуву, у Віженера 33 в степені довжини ключа
print("Кількість можливих ключів: Цезар", len(alphabet) - 1, "| Віженер (5 літер)", len(alphabet) ** 5)

letter, count = most_common_letter(text)
print("Найчастіша літера у тексті:", letter, count, "раз")
letter, count = most_common_letter(caesar_text)
print("Найчастіша літера у Цезарі:", letter, count, "раз")
letter, count = most_common_letter(vigenere_text)
print("Найчастіша літера у Віженері:", letter, count, "раз")

print()
brute_force(caesar_text)
