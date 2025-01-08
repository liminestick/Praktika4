import sqlite3
import csv

# Название файла
csv_file = "4/_product_data.csv"

# Подключение к базе данных
conn = sqlite3.connect("4/data4.db")
cursor = conn.cursor()

# Создаем таблицу с оптимальными типами данных, добавлена колонка category
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,             -- Название продукта
    price REAL NOT NULL,            -- Цена продукта
    quantity INTEGER NOT NULL,      -- Количество
    fromCity TEXT NOT NULL,         -- Город происхождения
    isAvailable BOOLEAN NOT NULL,   -- Наличие
    views INTEGER NOT NULL,         -- Просмотры
    category TEXT                   -- Тип товара (если есть)
)
""")
conn.commit()

# Считываем данные из CSV и добавляем в таблицу
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=";")
    header = next(reader)  # Пропускаем заголовок
    for row in reader:
        if len(row) == 0:  # Пропускаем пустые строки
            continue

        elif len(row) == 6:
            # Обрабатываем данные из строки
            name = row[0]
            price = float(row[1])
            quantity = int(row[2])
            fromCity = row[3]

            # Преобразуем строковые 'True'/'False' в булевое значение для поля isAvailable
            isAvailable = row[4].strip().lower() == "true"
            views = int(row[5])
            # Добавляем данные в таблицу
            cursor.execute("""
                INSERT INTO products (name, price, quantity, fromCity, isAvailable, category, views)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, price, quantity, fromCity, isAvailable, None, views))

        elif len(row) == 7:
            # Обрабатываем данные из строки
            name = row[0]
            price = float(row[1])
            quantity = int(row[2])
            category = row[3]
            fromCity = row[4]

            # Преобразуем строковые 'True'/'False' в булевое значение для поля isAvailable
            isAvailable = row[5].strip().lower() == "true"
            views = int(row[6])
            print(row)
            # Добавляем данные в таблицу
            cursor.execute("""
                INSERT INTO products (name, price, quantity, fromCity, isAvailable, category, views)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, price, quantity, fromCity, isAvailable, category, views))


conn.commit()
conn.close()

print("Данные успешно добавлены в базу данных data4.db.")
