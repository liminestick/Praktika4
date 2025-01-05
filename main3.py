import sqlite3
import csv
import pickle

# Создание базы данных и подключение к ней
conn = sqlite3.connect('3/data3.db')
cursor = conn.cursor()

# Создание таблицы (с оптимальными типами данных)
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    artist TEXT,
    song TEXT,
    duration_ms INTEGER,
    year INTEGER,
    tempo REAL,
    genre TEXT,
    energy REAL,
    key INTEGER,
    loudness REAL,
    popularity INTEGER
)
''')

# Подтверждение создания таблицы
conn.commit()

# Чтение CSV файла
file_path_csv = '3/_part_1.csv'

with open(file_path_csv, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')

    # Пропускаем заголовок
    headers = next(reader)

    # Чтение и подготовка данных для вставки
    for row in reader:
        # Пропускаем пустые строки
        if not row:
            continue

        # Если строка некорректная (меньше 9 элементов), добавляем недостающие значения как None
        row = row + [None] * (9 - len(row))

        # Преобразуем значения в соответствующие типы данных
        artist, song, duration_ms, year, tempo, genre, energy, key, loudness = row
        duration_ms = int(duration_ms) if duration_ms is not None else None
        year = int(year) if year is not None else None
        tempo = float(tempo) if tempo is not None else None
        energy = float(energy) if energy is not None else None
        key = int(key) if key is not None else None
        loudness = float(loudness) if loudness is not None else None

        # Вставка данных в таблицу
        cursor.execute('''
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, energy, key, loudness)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (artist, song, duration_ms, year, tempo, genre, energy, key, loudness))

# Подтверждение вставки данных
conn.commit()

# Чтение файла .pkl
file_path_pkl = '3/_part_2.pkl'

with open(file_path_pkl, mode='rb') as file:
    data = pickle.load(file)

    # Вставка данных из pickle в таблицу
    for item in data:
        artist = item.get('artist')
        song = item.get('song')
        duration_ms = int(item.get('duration_ms')) if item.get('duration_ms') else None
        year = int(item.get('year')) if item.get('year') else None
        tempo = float(item.get('tempo')) if item.get('tempo') else None
        genre = item.get('genre')
        energy = float(item.get('energy')) if item.get('energy') else None
        popularity = int(item.get('popularity')) if item.get('popularity') else None

        # Вставка данных в таблицу
        cursor.execute('''
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, energy, key, loudness, popularity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (artist, song, duration_ms, year, tempo, genre, energy, None, None, popularity))

# Подтверждение вставки данных
conn.commit()

# Закрытие соединения с базой данных
conn.close()
