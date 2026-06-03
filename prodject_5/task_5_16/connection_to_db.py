import psycopg2

import pandas as pd



try:

    # Устанавливаем соединение

    connection = psycopg2.connect(

        host="localhost",          # База в контейнере, но доступна через localhost

        port="5432",               # Порт из секции ports

        user="postgres",           # POSTGRES_USER

        password="example",        # POSTGRES_PASSWORD

        database="testdb"          # POSTGRES_DB

    )

    print("✓ Подключение установлено")
