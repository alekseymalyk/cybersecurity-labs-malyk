# ЛР3 Невидимі дані у власних файлах
# ховаю текст у картинці методом LSB (молодший біт кожного кольору)
# Малик Олексій, 6.04.122.010.23.1

import os
from PIL import Image

# що ховаю: ПІБ і дата народження
full_name = "Малик Олексій Сергійович"
birth_date = "23.12.2005"
my_message = full_name + ", " + birth_date

# скільки біт на початку картинки займає довжина повідомлення
LEN_BITS = 32


# текст -> рядок з нулів і одиниць
# кирилиця в utf-8 займає 2 байти на букву
def text_to_bits(text):
    data = text.encode("utf-8")
    bits = ""
    for b in data:
        bits = bits + format(b, "08b")
    return bits


# рядок з нулів і одиниць -> текст
def bits_to_text(bits):
    data = []
    byte = ""
    for bit in bits:
        byte = byte + bit
        if len(byte) == 8:
            data.append(int(byte, 2))
            byte = ""
    return bytes(data).decode("utf-8")


# ставлю в молодший біт числа value потрібний біт (0 або 1)
def set_last_bit(value, bit):
    if value % 2 == 1:
        value = value - 1     # спочатку роблю молодший біт нулем
    return value + int(bit)


def hide_message(in_path, out_path, text):
    img = Image.open(in_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    msg_bits = text_to_bits(text)
    # спочатку пишу довжину повідомлення в бітах, потім саме повідомлення
    bits = format(len(msg_bits), "0" + str(LEN_BITS) + "b") + msg_bits

    if len(bits) > width * height * 3:
        print("Повідомлення не влазить у картинку")
        return False

    k = 0
    for y in range(height):
        for x in range(width):
            if k >= len(bits):
                break
            r, g, b = pixels[x, y]
            # в кожен піксель влазить 3 біти: по одному в R, G і B
            if k < len(bits):
                r = set_last_bit(r, bits[k])
                k = k + 1
            if k < len(bits):
                g = set_last_bit(g, bits[k])
                k = k + 1
            if k < len(bits):
                b = set_last_bit(b, bits[k])
                k = k + 1
            pixels[x, y] = (r, g, b)

    # тільки png, бо jpg стискає картинку і молодші біти зіпсуються
    img.save(out_path, "PNG")
    return True


# читаю перші count молодших бітів картинки підряд: R, G, B, R, G, B ...
def read_bits(pixels, width, height, count):
    bits = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for value in (r, g, b):
                if len(bits) < count:
                    bits = bits + str(value % 2)
            if len(bits) >= count:
                return bits
    return bits


def extract_message(path):
    img = Image.open(path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    # спочатку довжина повідомлення
    length = int(read_bits(pixels, width, height, LEN_BITS), 2)
    if length > width * height * 3:
        return ""   # в картинці нічого не сховано

    # потім читаю все разом і пропускаю перші LEN_BITS біт
    all_bits = read_bits(pixels, width, height, LEN_BITS + length)
    msg_bits = ""
    i = 0
    for bit in all_bits:
        if i >= LEN_BITS:
            msg_bits = msg_bits + bit
        i = i + 1
    return bits_to_text(msg_bits)


# етап 1: показую по кроках, що відбувається з першою буквою
def show_steps(in_path, text):
    img = Image.open(in_path).convert("RGB")
    pixels = img.load()
    first = text[0]
    print("Перша буква:", first)
    print("Байти utf-8:", list(first.encode("utf-8")))
    print("Біти:       ", text_to_bits(first))
    print("Перші 3 пікселі до приховування:")
    for x in range(3):
        print("  ", pixels[x, 0])
    print("Число 200 = " + format(200, "08b") + ", якщо записати біт 1 -> "
          + str(set_last_bit(200, "1")) + " = " + format(set_last_bit(200, "1"), "08b"))


# етап 4: порівнюю оригінал і картинку з повідомленням
def compare(orig_path, stego_path, diff_path):
    a = Image.open(orig_path).convert("RGB")
    b = Image.open(stego_path).convert("RGB")
    pa = a.load()
    pb = b.load()
    width, height = a.size

    diff = Image.new("RGB", (width, height), (0, 0, 0))
    pd = diff.load()
    changed = 0
    changed_r = 0
    changed_g = 0
    changed_b = 0
    max_diff = 0
    for y in range(height):
        for x in range(width):
            r1, g1, b1 = pa[x, y]
            r2, g2, b2 = pb[x, y]
            if r1 != r2:
                changed_r = changed_r + 1
            if g1 != g2:
                changed_g = changed_g + 1
            if b1 != b2:
                changed_b = changed_b + 1
            if r1 != r2 or g1 != g2 or b1 != b2:
                changed = changed + 1
                pd[x, y] = (255, 255, 255)   # змінений піксель білим
            for d in (abs(r1 - r2), abs(g1 - g2), abs(b1 - b2)):
                if d > max_diff:
                    max_diff = d
    diff.save(diff_path)

    total = width * height
    print("Розмір картинки:", width, "x", height, "=", total, "пікселів")
    print("Розмір файлу до: ", os.path.getsize(orig_path), "байт")
    print("Розмір файлу після:", os.path.getsize(stego_path), "байт")
    print("Змінено пікселів:", changed, "(" + str(round(changed * 100 / total, 3)) + " %)")
    print("По каналах: R =", changed_r, " G =", changed_g, " B =", changed_b)
    print("Найбільша зміна кольору:", max_diff, "з 255")


print("=== ЛР3: приховування тексту в картинці (LSB) ===")
path = input("Картинка (Enter = images/original.png): ")
if path == "":
    path = "images/original.png"
text = input("Текст (Enter = моє ПІБ і дата народження): ")
if text == "":
    text = my_message

print()
print("--- Як це працює ---")
show_steps(path, text)

print()
print("--- Приховування ---")
print("Текст:", text)
print("Символів:", len(text), " байт:", len(text.encode("utf-8")),
      " біт:", len(text_to_bits(text)), "+", LEN_BITS, "біт на довжину")
ok = hide_message(path, "images/stego.png", text)
if ok:
    print("Збережено: images/stego.png")

    print()
    print("--- Витягування ---")
    found = extract_message("images/stego.png")
    print("Знайдено:", found)
    if found == text:
        print("Текст збігається з оригіналом")
    else:
        print("Текст НЕ збігається")

    print()
    print("--- Порівняння ---")
    compare(path, "images/stego.png", "images/diff.png")
    print("Карта змін: images/diff.png")
