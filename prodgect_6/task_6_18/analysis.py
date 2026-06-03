import psycopg2

import pandas as pd
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

try:

    # Устанавливаем соединение

    connection = psycopg2.connect(

        host="localhost",          # База в контейнере, но доступна через localhost

        port="5434",               # Порт из секции ports

        user="postgres",           # POSTGRES_USER

        password="student",        # POSTGRES_PASSWORD

        database="student_task"          # POSTGRES_DB

    )

    print("✓ Подключение установлено")

except Exception as error:

    print(f"Ошибка при подключении: {error}")

query = """
SELECT 
    pr.price, 
    p.name AS product_name, 
    p.category
FROM 
    prices pr
JOIN 
    products p ON pr.product_id = p.id;
"""

try:
    df = pd.read_sql_query(query, connection)
    print(df.head(200))
except Exception as e:
     print(f"Ошибка выполнения запроса: {e}")

stats = df['price'].agg(['mean', 'median', 'std', 'min', 'max'])

print(f"Среднее значение: {stats['mean']:.2f} руб.")
print(f"Медиана: {stats['median']:.2f} руб.")
print(f"Стандартное отклонение: {stats['std']:.2f} руб.")
print(f"Минимальная цена: {stats['min']:.2f} руб.")
print(f"Максимальная цена: {stats['max']:.2f} руб.")

q1 = df['price'].quantile(0.25)
q2 = df['price'].median()
q3 = df['price'].quantile(0.75)
iqr = q3 - q1

print(f"Q1: {q1:.2f} руб., Q2 (медиана): {q2:.2f} руб., Q3: {q3:.2f} руб.")
print(f"IQR: {iqr:.2f} руб.")

# Товары с ценой выше Q3
expensive_items = df[df['price'] > q3][['product_name', 'category', 'price']]
print("\nТовары с ценой выше Q3:")
print(expensive_items)

category_stats = df.groupby('category')['price'].agg(['count', 'mean', 'median', 'std'])
category_stats = category_stats.sort_values(by='mean', ascending=False)

print("Статистика по категориям:")
print(category_stats)

# Группировка по названию товара и расчёт разницы между max и min
price_range = df.groupby('product_name')['price'].agg(['min', 'max'])
price_range['diff'] = price_range['max'] - price_range['min']

# Топ-5 товаров с наибольшим разбросом
top_5_spread = price_range.sort_values(by='diff', ascending=False).head(5)
print("Топ-5 товаров с наибольшим разбросом цен:")
print(top_5_spread)



