import json
import sqlite3
import statistics
from collections import Counter

# Имя файла JSON
json_file = "1-2/item.json"

# Имя базы данных
db_name = "1-2/data.db"

# Подключение к базе данных
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS FirstTable (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    street TEXT,
    city TEXT,
    zipcode INTEGER,
    floors INTEGER,
    year INTEGER,
    parking BOOLEAN,
    prob_price REAL,
    views INTEGER
)
''')

# Чтение JSON файла
with open(json_file, 'r', encoding='utf-8') as file:
    # Загружаем весь JSON как список объектов
    data = json.load(file)

    for record in data:
        cursor.execute('''
        INSERT INTO FirstTable (id, name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES (:id, :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views)
        ''', record)

# Сохраняем изменения
conn.commit()
conn.close()

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Функция для выполнения заданий
# Задание 1: Вывод первых (89) строк, отсортированных по числовому полю (views), в файл формата JSON
cursor.execute('SELECT * FROM FirstTable ORDER BY views LIMIT 89')
rows = cursor.fetchall()
data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
with open("1-2/sorted_by_views.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Задание 2: Вывод суммы, минимального, максимального и среднего значения для числового поля (prob_price)
cursor.execute('SELECT prob_price FROM FirstTable')
prob_prices = [row[0] for row in cursor.fetchall()]
total = sum(prob_prices)
minimum = min(prob_prices)
maximum = max(prob_prices)
avg = statistics.mean(prob_prices)
print(f"Задание 2: prob_price — Сумма: {total}, Минимум: {minimum}, Максимум: {maximum}, Среднее: {avg}")

# Задание 3: Вывод частоты встречаемости для категориального поля (city)
cursor.execute('SELECT city FROM FirstTable')
cities = [row[0] for row in cursor.fetchall()]
city_frequency = Counter(cities)
print("Задание 3: Частота встречаемости для поля 'city':")
for city, freq in city_frequency.items():
    print(f"{city}: {freq}")

# Задание 4: Вывод первых (89) строк, отфильтрованных по предикату (floors > 5),
# отсортированных по числовому полю (views), в файл формата JSON
cursor.execute('SELECT * FROM FirstTable WHERE floors > 5 ORDER BY views LIMIT 89')
rows = cursor.fetchall()
filtered_data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
with open("1-2/filtered_by_floors.json", "w", encoding="utf-8") as json_file:
    json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

# Закрытие соединения
conn.close()

