import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('4/data4.db')
cursor = conn.cursor()

# Топ-10 самых обновляемых товаров:
print('Топ-10 самых обновляемых товаров:')
cursor.execute('''
SELECT product_name, MAX(update_count) as max_updates
FROM updates
GROUP BY product_name
ORDER BY max_updates DESC
LIMIT 10;
''')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Анализ цен товаров:
print('Анализ цен товаров:')
cursor.execute('''
SELECT category, 
       COUNT(*) as product_count,
       SUM(price) as total_price,
       MIN(price) as min_price,
       MAX(price) as max_price,
       AVG(price) as avg_price
FROM products
GROUP BY category;
''')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Анализ остатков товаров:
print('Анализ остатков товаров:')
cursor.execute('''
SELECT category, 
       COUNT(*) as product_count,
       SUM(quantity) as total_quantity,
       MIN(quantity) as min_quantity,
       MAX(quantity) as max_quantity,
       AVG(quantity) as avg_quantity
FROM products
GROUP BY category;
''')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Произвольный запрос:
# Вывод товаров с ценой выше среднего в их категории
print('Вывод товаров с ценой выше среднего в их категории:')
cursor.execute('''
SELECT p.name, p.price, p.category
FROM products p
JOIN (
    SELECT category, AVG(price) as avg_price
    FROM products
    GROUP BY category
) cat_avg ON p.category = cat_avg.category
WHERE p.price > cat_avg.avg_price;
''')
rows = cursor.fetchall()
for row in rows:
    print(row)


cursor.close()