import sqlite3

# Имя базы данных
db_name = "1-2/data.db"

# Подключение к базе данных
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Очистка таблицы
cursor.execute("DELETE FROM FirstTable")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()