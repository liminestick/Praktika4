import sqlite3
import pickle

# Имя базы данных и pkl-файла
db_name = "1-2/data.db"
pkl_file = "1-2/subitem.pkl"  # Замените на имя вашего pkl-файла

# Подключение к базе данных
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Создаем таблицу SecondTable
cursor.execute('''
CREATE TABLE IF NOT EXISTS SecondTable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating REAL,
    convenience INTEGER,
    security INTEGER,
    functionality INTEGER,
    comment TEXT
)
''')

# Чтение данных из pkl-файла
with open(pkl_file, "rb") as file:
    data = pickle.load(file)

# Добавление данных в SecondTable
for record in data:
    cursor.execute('''
    INSERT INTO SecondTable (name, rating, convenience, security, functionality, comment)
    VALUES (:name, :rating, :convenience, :security, :functionality, :comment)
    ''', record)

# Сохранение изменений
conn.commit()
conn.close()

