# Лабораторна робота 2. Шифр Цезаря і шифр Віженера
# Автор: Малик Олексій

# український алфавіт (33 літери)
alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

# мої дані для ключів
birth_date = "23.12.2005"
surname = "малик"

# мій текст для перевірки
my_text = "Зустрінемось біля бібліотеки ХНЕУ о пів на третю"


def make_caesar_key(date):
    # зсув = сума цифр дати народження
    total = 0
    for c in date:
        if c.isdigit():
            total = total + int(c)
    return total


def shift_letter(c, shift):
    # зсуває одну літеру по алфавіту, інші символи не змінює
    low = c.lower()
    if low not in alphabet:
        return c
    pos = alphabet.index(low)
    new_pos = (pos + shift) % len(alphabet)
    new_letter = alphabet[new_pos]
    if c.isupper():
        new_letter = new_letter.upper()
    return new_letter


def caesar_encrypt(text, shift):
    result = ""
    for c in text:
        result = result + shift_letter(c, shift)
    return result


def caesar_decrypt(text, shift):
    result = ""
    for c in text:
        result = result + shift_letter(c, -shift)
    return result


def vigenere(text, key, direction):
    # direction = 1 для шифрування, -1 для розшифрування
    result = ""
    key_index = 0
    for c in text:
        if c.lower() in alphabet:
            key_letter = key[key_index % len(key)]
            shift = alphabet.index(key_letter)
            result = result + shift_letter(c, shift * direction)
            key_index = key_index + 1
        else:
            result = result + c
    return result


def vigenere_encrypt(text, key):
    return vigenere(text, key, 1)


def vigenere_decrypt(text, key):
    return vigenere(text, key, -1)


def most_common_letter(text):
    # частотний аналіз: яка літера зустрічається найчастіше
    best_letter = ""
    best_count = 0
    for letter in alphabet:
        count = text.lower().count(letter)
        if count > best_count:
            best_count = count
            best_letter = letter
    return best_letter, best_count


def brute_force(text):
    # перебираємо всі можливі зсуви шифру Цезаря
    print("Злом шифру Цезаря перебором:")
    for shift in range(1, len(alphabet)):
        print(shift, caesar_decrypt(text, shift))


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

print()
print("Порівняння:")
print("Довжина тексту:", len(text), "| Цезар:", len(caesar_text), "| Віженер:", len(vigenere_text))
print("Кількість можливих ключів: Цезар", len(alphabet) - 1, "| Віженер (5 літер)", len(alphabet) ** 5)

letter, count = most_common_letter(text)
print("Найчастіша літера у тексті:", letter, count, "раз")
letter, count = most_common_letter(caesar_text)
print("Найчастіша літера у Цезарі:", letter, count, "раз")
letter, count = most_common_letter(vigenere_text)
print("Найчастіша літера у Віженері:", letter, count, "раз")

print()
brute_force(caesar_text)
