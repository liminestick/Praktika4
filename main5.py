import sqlite3
import csv


# Функция для чтения XML вручную
def parse_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Простая обработка XML вручную
    users = []
    current_user = {}
    for line in lines:
        line = line.strip()
        if "<Sheet1>" in line:
            current_user = {}
        elif "</Sheet1>" in line:
            users.append(current_user)
        elif "<name>" in line:
            current_user["name"] = line.replace("<name>", "").replace("</name>", "")
        elif "<phoneNumber>" in line:
            current_user["phoneNumber"] = line.replace("<phoneNumber>", "").replace("</phoneNumber>", "")
        elif "<email>" in line:
            current_user["email"] = line.replace("<email>", "").replace("</email>", "")
        elif "<address>" in line:
            current_user["address"] = line.replace("<address>", "").replace("</address>", "")
        elif "<userAgent>" in line:
            current_user["userAgent"] = line.replace("<userAgent>", "").replace("</userAgent>", "")
        elif "<hexcolor>" in line:
            current_user["hexcolor"] = line.replace("<hexcolor>", "").replace("</hexcolor>", "")
    return users


# Создание базы данных и таблиц
conn = sqlite3.connect("5/data5.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phoneNumber TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS addresses (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS metadata (
    metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    userAgent TEXT,
    hexcolor TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
""")

# Парсинг и добавление данных из CSV
with open("5/users.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("INSERT INTO users (name, phoneNumber, email) VALUES (?, ?, ?)",
                       (row["name"], row["phoneNumber"], row["email"]))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO addresses (user_id, address) VALUES (?, ?)", (user_id, row["address"]))
        cursor.execute("INSERT INTO metadata (user_id, userAgent, hexcolor) VALUES (?, ?, ?)",
                       (user_id, row["userAgent"], row["hexcolor"]))

# Парсинг и добавление данных из XML
xml_data = parse_xml("5/users.xml")
for user in xml_data:
    cursor.execute("INSERT INTO users (name, phoneNumber, email) VALUES (?, ?, ?)",
                   (user["name"], user["phoneNumber"], user["email"]))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO addresses (user_id, address) VALUES (?, ?)", (user_id, user["address"]))
    cursor.execute("INSERT INTO metadata (user_id, userAgent, hexcolor) VALUES (?, ?, ?)",
                   (user_id, user["userAgent"], user["hexcolor"]))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Данные успешно добавлены в базу данных.")
