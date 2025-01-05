import sqlite3

# Подключение к базе данных
db_name = "1-2/data.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# 1. Запрос: Соединение данных по совпадающим названиям зданий (name)
print("1. Совпадающие здания в обеих таблицах:")
cursor.execute('''
SELECT ft.id, ft.name, ft.city, st.rating, st.comment
FROM FirstTable ft
JOIN SecondTable st ON ft.name = st.name
''')
result = cursor.fetchall()
for row in result:
    print(row)

# 2. Запрос: Список зданий из FirstTable с рейтингом из SecondTable выше 4.0
print("\n2. Здания с высоким рейтингом:")
cursor.execute('''
SELECT ft.name, ft.city, st.rating
FROM FirstTable ft
JOIN SecondTable st ON ft.name = st.name
WHERE st.rating > 4.0
''')
result = cursor.fetchall()
for row in result:
    print(row)

# 3. Запрос: Здания с городом и его максимальным рейтингом
print("\n3. Здания с рейтингом  :")
cursor.execute('''
SELECT f.name AS building_name, f.city, MAX(s.rating) AS max_rating
FROM FirstTable f
LEFT JOIN SecondTable s ON f.name = s.name
GROUP BY f.name, f.city''')
result = cursor.fetchall()
for row in result:
    print(row)
cursor.close()