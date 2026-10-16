# ЛР4 Особистий цифровий підпис
# спрощена система підпису: SHA-256 + маленький RSA з ключами з моїх даних
# Малик Олексій, 6.04.122.010.23.1

import hashlib
import os

# з чого роблю ключі
full_name = "Малик Олексій Сергійович"
birth_date = "23.12.2005"
secret_word = "zhovtyi_tramvai_27"

# стандартна відкрита експонента як у справжньому RSA
E = 65537


# перевірка на просте число звичайним перебором дільників
def is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i = i + 1
    return True


# наступне просте число після x
def next_prime(x):
    while not is_prime(x):
        x = x + 1
    return x


# найбільший спільний дільник
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# генерація пари ключів з ПІБ + дати народження + секретного слова
def make_keys(name, date, word):
    h = hashlib.sha256((name + date + word).encode("utf-8")).hexdigest()
    print("SHA-256 від (ПІБ + дата + слово):", h)
    # з хешу беру два шматки по 8 символів і шукаю від них прості числа
    p = next_prime(int(h[0:8], 16))
    q = next_prime(int(h[8:16], 16))
    phi = (p - 1) * (q - 1)
    while gcd(E, phi) != 1:
        q = next_prime(q + 1)
        phi = (p - 1) * (q - 1)
    n = p * q
    d = pow(E, -1, phi)   # приватний ключ: обернене до E за модулем phi
    print("p =", p, " q =", q)
    print("n = p * q =", n)
    return d, n


def save_key(path, a, n):
    f = open(path, "w")
    f.write(str(a) + "\n" + str(n) + "\n")
    f.close()


def load_key(path):
    f = open(path)
    lines = f.read().split()
    f.close()
    return int(lines[0]), int(lines[1])


# SHA-256 від вмісту файлу
def file_hash(path):
    f = open(path, "rb")
    data = f.read()
    f.close()
    return hashlib.sha256(data).hexdigest()


# підпис: хеш документа "шифрую" приватним ключем
def sign_file(path, d, n):
    h = int(file_hash(path), 16) % n
    signature = pow(h, d, n)
    f = open(path + ".sig", "w")
    f.write(str(signature) + "\n")
    f.close()
    return signature


# перевірка: розшифровую підпис публічним ключем і порівнюю з хешем файлу зараз
def verify_file(path, sig_path, e, n):
    f = open(sig_path)
    signature = int(f.read())
    f.close()
    from_signature = pow(signature, e, n)
    now = int(file_hash(path), 16) % n
    print("  хеш з підпису:   ", from_signature)
    print("  хеш файлу зараз: ", now)
    if from_signature == now:
        print("  Підпис ДІЙСНИЙ")
        return True
    print("  Підпис ПІДРОБЛЕНИЙ")
    return False


def copy_file(src, dst):
    f = open(src, "rb")
    data = f.read()
    f.close()
    f = open(dst, "wb")
    f.write(data)
    f.close()


print("=== ЛР4: особистий цифровий підпис ===")
word = input("Секретне слово (Enter = моє): ")
if word == "":
    word = secret_word
doc = input("Документ (Enter = documents/dovidka.txt): ")
if doc == "":
    doc = "documents/dovidka.txt"

print()
print("--- Крок 2. Генерація ключів ---")
d, n = make_keys(full_name, birth_date, word)
os.makedirs("keys", exist_ok=True)
save_key("keys/private.key", d, n)
save_key("keys/public.key", E, n)
print("Приватний ключ (d, n) -> keys/private.key")
print("Публічний ключ (e, n) -> keys/public.key, e =", E)

print()
print("--- Крок 3. Підписання ---")
print("SHA-256 документа:", file_hash(doc))
signature = sign_file(doc, d, n)
print("Підпис:", signature)
print("Збережено:", doc + ".sig")
print("Перевірка публічним ключем:")
e, n_pub = load_key("keys/public.key")
verify_file(doc, doc + ".sig", e, n_pub)

print()
print("--- Крок 4.1. Змінюю документ ---")
fake_doc = doc.replace(".txt", "_changed.txt")
copy_file(doc, fake_doc)
f = open(fake_doc, "a", encoding="utf-8")
f.write("Оцінка: 100 балів\n")
f.close()
print("Дописав рядок у", fake_doc, "і перевіряю старим підписом:")
verify_file(fake_doc, doc + ".sig", e, n_pub)

print()
print("--- Крок 4.3. Підробка підпису без мого приватного ключа ---")
print("Хтось знає моє ПІБ і дату, але не знає секретне слово:")
d_fake, n_fake = make_keys(full_name, birth_date, "qwerty")
fake_sig = pow(int(file_hash(fake_doc), 16) % n_pub, d_fake, n_pub)
f = open(fake_doc + ".sig", "w")
f.write(str(fake_sig) + "\n")
f.close()
print("Підписав змінений документ своїм ключем, перевіряю моїм публічним:")
verify_file(fake_doc, fake_doc + ".sig", e, n_pub)
