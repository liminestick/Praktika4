import sqlite3
import json

# Подключаемся к базе данных
conn = sqlite3.connect('3/data3.db')
cursor = conn.cursor()

# 1. Вывод первых (89) отсортированных по произвольному числовому полю строк из таблицы в файл формата json
cursor.execute('''
SELECT * FROM songs ORDER BY duration_ms DESC LIMIT 89
''')
rows = cursor.fetchall()

# Преобразуем результат в формат json
result_json = []
for row in rows:
    result_json.append({
        'artist': row[0],
        'song': row[1],
        'duration_ms': row[2],
        'year': row[3],
        'tempo': row[4],
        'genre': row[5],
        'energy': row[6],
        'key': row[7],
        'loudness': row[8],
        'popularity': row[9]
    })

# Сохраняем результат в файл json
with open('3/songs_89_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(result_json, f, ensure_ascii=False, indent=4)

# 2. Вывод (сумму, мин, макс, среднее) по произвольному числовому полю tempo
cursor.execute('''
SELECT SUM(tempo), MIN(tempo), MAX(tempo), AVG(tempo) FROM songs
''')
tempo_stats = cursor.fetchone()
print(f"Сумма: {tempo_stats[0]}, Минимум: {tempo_stats[1]}, Максимум: {tempo_stats[2]}, Среднее: {tempo_stats[3]}")

# 3. Вывод частоты встречаемости для категориального поля жанра
cursor.execute('''
SELECT genre, COUNT(*) FROM songs GROUP BY genre ORDER BY COUNT(*) DESC
''')
genre_frequency = cursor.fetchall()

print("Частота встречаемости жанров:")
for genre, count in genre_frequency:
    print(f"{genre}: {count}")

# 4. Вывод первых (94) отфильтрованных по произвольному предикату по году >= 2010
# Отсортируем по tempo
cursor.execute('''
SELECT * FROM songs WHERE year >= 2010 ORDER BY tempo DESC LIMIT 94
''')
filtered_rows = cursor.fetchall()

# Преобразуем результат в формат json
filtered_result_json = []
for row in filtered_rows:
    filtered_result_json.append({
        'artist': row[0],
        'song': row[1],
        'duration_ms': row[2],
        'year': row[3],
        'tempo': row[4],
        'genre': row[5],
        'energy': row[6],
        'key': row[7],
        'loudness': row[8],
        'popularity': row[9]
    })

# Сохраняем результат в файл json
with open('3/songs_94_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_result_json, f, ensure_ascii=False, indent=4)

# Закрытие соединения с базой данных
conn.close()
