# Лабораторна робота 1. Перевірка пароля на особисті дані
# Автор: Малик Олексій

# мої особисті дані (латиницею, як їх зазвичай пишуть у паролях)
name = "oleksii"
short_name = "olek"
surname = "malyk"
birth_day = "23"
birth_month = "12"
birth_year = "2005"

# популярні комбінації, які часто використовують у паролях
popular = ["123456", "qwerty", "password", "admin", "1111"]

# спеціальні символи
special_chars = "!@#$%^&*()-_=+.,?"


def check_password(password):
    score = 10
    tips = []
    low = password.lower()

    # 1. перевірка довжини
    if len(password) < 8:
        score = score - 3
        tips.append("Пароль занадто короткий, потрібно хоча б 8 символів")
    elif len(password) < 12:
        score = score - 1
        tips.append("Краще зробити пароль довшим за 12 символів")

    # 2. перевірка типів символів
    has_digit = False
    has_upper = False
    has_special = False

    for c in password:
        if c.isdigit():
            has_digit = True
        if c.isupper():
            has_upper = True
        if c in special_chars:
            has_special = True

    if has_digit == False:
        score = score - 1
        tips.append("Додайте цифри")
    if has_upper == False:
        score = score - 1
        tips.append("Додайте великі літери")
    if has_special == False:
        score = score - 1
        tips.append("Додайте спеціальні символи")

    # 3. перевірка особистих даних
    if name in low or short_name in low:
        score = score - 3
        tips.append("У паролі є ваше ім'я")

    if surname in low:
        score = score - 3
        tips.append("У паролі є ваше прізвище")

    if birth_year in low:
        score = score - 2
        tips.append("У паролі є рік народження")

    day_and_month = birth_day + birth_month
    if day_and_month in low:
        score = score - 2
        tips.append("У паролі є день і місяць народження")

    # 4. перевірка популярних комбінацій
    for word in popular:
        if word in low:
            score = score - 3
            tips.append("У паролі є популярна комбінація " + word)

    # оцінка не може бути менше 1
    if score < 1:
        score = 1

    return score, tips


print("Перевірка пароля")
password = input("Введіть пароль: ")

score, tips = check_password(password)

print("Оцінка:", score, "з 10")

if score <= 4:
    print("Пароль слабкий")
elif score <= 7:
    print("Пароль середній")
else:
    print("Пароль надійний")

if len(tips) > 0:
    print("Рекомендації:")
    for tip in tips:
        print("-", tip)
