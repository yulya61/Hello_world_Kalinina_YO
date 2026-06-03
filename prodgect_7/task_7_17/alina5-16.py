import psycopg2

DB_HOST     = "localhost"
DB_PORT     = "5434"
DB_USER     = "postgres"
DB_PASSWORD = "student"
DB_NAME     = "student_task"

try:
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM products;"
    cursor.execute(query)

    count = cursor.fetchone()[0]
    print(f"Количество товаров: {count}")

except Exception as error:
    print(error)

finally:
    cursor.close()
    connection.close()