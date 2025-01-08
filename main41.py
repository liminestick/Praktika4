import sqlite3
import msgpack

# Подключение к базе данных
conn = sqlite3.connect("4/data4.db")
cursor = conn.cursor()

# Создание таблицы updates
cursor.execute("""
CREATE TABLE IF NOT EXISTS updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    method TEXT NOT NULL,
    param REAL NOT NULL,
    update_count INTEGER DEFAULT 0
)
""")
conn.commit()

# Путь к файлу .msgpack
msgpack_file = "4/_update_data.msgpack"

# Чтение файла .msgpack
with open(msgpack_file, "rb") as file:
    updates = msgpack.unpack(file, raw=False)

# Запись данных в таблицу updates
for update in updates:
    cursor.execute("""
        INSERT INTO updates (product_name, method, param)
        VALUES (?, ?, ?)
    """, (update['name'], update['method'], update['param']))
conn.commit()
print("Обновления успешно добавлены в таблицу updates.")

# Обработка обновлений
# Обработка обновлений
for update in updates:
    product_name = update['name']
    method = update['method']
    param = update['param']

    # Используем контекстный менеджер для транзакции
    try:
        with conn:
            # Получаем текущие данные о продукте
            cursor.execute("SELECT price, quantity FROM products WHERE name = ?", (product_name,))
            result = cursor.fetchone()

            if not result:
                print(f"Продукт {product_name} не найден.")
                continue

            price, quantity = result

            # Обрабатываем метод обновления
            if method == "price_abs":
                price = param
            elif method == "price_percent":
                price += price * param
            elif method == "quantity_add":
                quantity += int(param)
            elif method == "quantity_sub":
                quantity += int(param)
            elif method == "remove":
                cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
                continue
            elif method == "available":
                cursor.execute("UPDATE products SET isAvailable = ? WHERE name = ?", (param, product_name))
                continue

            # Проверяем корректность данных
            if price < 0 or quantity < 0:
                raise ValueError("Цена или остатки не могут быть отрицательными.")

            # Обновляем продукт
            cursor.execute("""
                UPDATE products
                SET price = ?, quantity = ?
                WHERE name = ?
            """, (price, quantity, product_name))

            # Увеличиваем счетчик обновлений
            cursor.execute("""
                UPDATE updates
                SET update_count = update_count + 1
                WHERE product_name = ?
            """, (product_name,))
    except Exception as e:
        print(f"Ошибка при обработке {product_name}: {e}")

