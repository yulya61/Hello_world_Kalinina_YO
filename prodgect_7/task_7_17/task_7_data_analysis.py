import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Отключаем предупреждения Pandas о типе подключения DBAPI2, чтобы логи были чистыми
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

# Настройка глобальных стилей графиков
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 10, 
    'figure.titlesize': 14,
    'axes.labelsize': 11,
    'axes.titlesize': 12
})

def get_connection():
    """Создает подключение к PostgreSQL на основе параметров Docker."""
    import psycopg2
    db_params = {
        "dbname": "student_task",
        "user": "postgres",
        "password": "student",
        "host": "localhost",
        "port": "5434"
    }
    return psycopg2.connect(**db_params)

def check_and_populate_db():
    """Проверяет наличие данных и аккуратно заполняет БД при их отсутствии."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM products;")
        if cursor.fetchone() == 0:
            print("Таблицы пусты. Генерируем чистые демонстрационные данные...")
            
            # Продукты
            products = [
                ('Смартфон X', 'Электроника'), ('Ноутбук Pro', 'Электроника'),
                ('Джинсы Slim', 'Одежда'), ('Куртка Winter', 'Одежда'),
                ('Изучаем Python', 'Книги'), ('Алгоритмы', 'Книги'),
                ('Диван Комфорт', 'Дом'), ('Стол Рабочий', 'Дом')
            ]
            for name, cat in products:
                cursor.execute("INSERT INTO products (name, category) VALUES (%s, %s);", (name, cat))
            
            # Исторические цены
            np.random.seed(42)
            cursor.execute("SELECT id, category FROM products;")
            rows = cursor.fetchall()
            dates = pd.date_range(start="2026-01-01", periods=15, freq="D")
            cat_bases = {'Электроника': 50000, 'Одежда': 4000, 'Книги': 1500, 'Дом': 12000}
            
            for prod_id, cat in rows:
                base = cat_bases.get(cat, 5000)
                for date in dates:
                    price = float(base + np.random.normal(0, base * 0.08))
                    if np.random.rand() < 0.04:
                        price *= 6
                    cursor.execute(
                        "INSERT INTO prices (product_id, price, created_at) VALUES (%s, %s, %s);",
                        (prod_id, price, date.strftime('%Y-%m-%d %H:%M:%S'))
                    )
            conn.commit()
            print("Данные успешно сгенерированы.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка инициализации: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    try:
        check_and_populate_db()
    except Exception:
        pass

    conn = get_connection()
    
    # Набор 1: Исторические цены (Для гистограммы, расчета метрик, аномалий и Boxplot)
    query_history = """
        SELECT pr.price, p.category, pr.created_at::date as price_date
        FROM prices pr
        JOIN products p ON pr.product_id = p.id;
    """
    df_history = pd.read_sql_query(query_history, conn)
    df_history['price'] = df_history['price'].astype(float)

    # Набор 2: Актуальная совокупная стоимость по категориям (Для круговой диаграммы)
    query_total_cost = """
        WITH latest_prices AS (
            SELECT DISTINCT ON (product_id) product_id, price
            FROM prices
            ORDER BY product_id, created_at DESC
        )
        SELECT p.category, SUM(lp.price)::numeric(10,2) AS total_category_cost
        FROM latest_prices lp
        JOIN products p ON lp.product_id = p.id
        GROUP BY p.category;
    """
    df_total_cost = pd.read_sql_query(query_total_cost, conn)
    df_total_cost['total_category_cost'] = df_total_cost['total_category_cost'].astype(float)

    # Набор 3: Зависимость средней цены от категории (Для столбчатой диаграммы)
    query_category_avg = """
        SELECT p.category, AVG(pr.price)::numeric(10,2) AS avg_price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        GROUP BY p.category
        ORDER BY avg_price DESC;
    """
    df_cat_avg = pd.read_sql_query(query_category_avg, conn)
    df_cat_avg['avg_price'] = df_cat_avg['avg_price'].astype(float)
    
    conn.close()

    # РАСЧЕТ СТАТИСТИЧЕСКИХ МЕТРИК
    mean_price = df_history['price'].mean()
    median_price = df_history['price'].median()
    
    # Расчет дисперсии и среднеквадратического отклонения
    variance_price = df_history['price'].var()
    std_dev_price = df_history['price'].std()
    
    q1 = df_history['price'].quantile(0.25)
    q3 = df_history['price'].quantile(0.75)
    iqr = q3 - q1
    
    # Математический расчет точных границ усов
    lower_bound = max(df_history['price'].min(), q1 - 1.5 * iqr)
    upper_bound = q3 + 1.5 * iqr
    
    anomalies = df_history[df_history['price'] > upper_bound]

    # Инициализация сетки 2х2
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("Визуализация данных учебной БД", fontweight='bold', y=0.98)

    # ----------------------------------------------------
    # СТРОКА 1, ОКНО 1: Распределение цен товаров
    # ----------------------------------------------------
    ax1 = axes[0, 0]
    sns.histplot(
        data=df_history, 
        x='price', 
        kde=True, 
        ax=ax1, 
        color='darkslateblue', 
        bins=30, 
        binrange=(0, 75000),
        legend=False
    )
    intervals = np.arange(0, 80000, 10000)
    ax1.set_xticks(intervals)
    ax1.set_xticklabels([f"{int(x)}" for x in intervals])

    # Нанесение вертикальных линий метрик центральной тенденции
    ax1.axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_price:.1f}')
    ax1.axvline(median_price, color='green', linestyle='-', linewidth=2, label=f'Медиана: {median_price:.1f}')
    
    # Элементы для вывода дисперсии и отклонения в легенду графика
    ax1.plot([], [], ' ', label=f'Дисперсия: {variance_price:.1f}')
    ax1.plot([], [], ' ', label=f'Ср. откл. (Std): ±{std_dev_price:.1f}')

    ax1.set_title("1. Распределение цен товаров (Основной диапазон)", fontweight='semibold')
    ax1.set_xlabel("Цена товара (руб.)")
    ax1.set_ylabel("Количество записей")
    ax1.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='lightgray')

    # ----------------------------------------------------
    # СТРОКА 1, ОКНО 2: Совокупная актуальная стоимость по категориям
    # ----------------------------------------------------
    ax2 = axes[0, 1]
    ax2.pie(
        df_total_cost['total_category_cost'], 
        labels=df_total_cost['category'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=sns.color_palette('Set2', len(df_total_cost)),
        textprops={'fontsize': 10}
    )
    ax2.set_title("2. Совокупная стоимость по категориям", fontweight='semibold')

    # ----------------------------------------------------
    # СТРОКА 2, ОКНО 1: Зависимость средней цены от категории
    # ----------------------------------------------------
    ax3 = axes[1, 0]
    if not df_cat_avg.empty:
        sns.barplot(data=df_cat_avg, x='category', y='avg_price', ax=ax3, palette='viridis', hue='category', legend=False)
        ax3.set_title("3. Зависимость средней цены от категории", fontweight='semibold')
        ax3.set_xlabel("Категория товара")
        ax3.set_ylabel("Средняя цена (руб.)")
        
        # Наклон 30 градусов и правое выравнивание подписей оси X
        ax3.tick_params(axis='x', labelsize=9, labelrotation=30)
        for tick in ax3.get_xticklabels():
            tick.set_horizontalalignment('right')
    else:
        ax3.text(0.5, 0.5, 'Нет данных по категориям', ha='center', va='center', fontsize=12)

    # ----------------------------------------------------
    # СТРОКА 2, ОКНО 2: Boxplot С КВАРТИЛЯМИ И ГРАНИЦАМИ УСОВ
    # ----------------------------------------------------
    ax4 = axes[1, 1]
    sns.boxplot(data=df_history, y='price', ax=ax4, color='lightblue', width=0.4)
    ax4.set_yscale('log')
    
    from matplotlib.ticker import ScalarFormatter
    ax4.yaxis.set_major_formatter(ScalarFormatter())
    ax4.ticklabel_format(style='plain', axis='y')
    
    # Линии и подписи для усов
    ax4.axhline(upper_bound, color='royalblue', linestyle='-.', linewidth=1.5)
    ax4.text(0.25, upper_bound, f' Верхний ус: {upper_bound:.1f} руб.', color='mediumblue', va='center', fontweight='semibold')
    
    ax4.axhline(lower_bound, color='royalblue', linestyle='-.', linewidth=1.5)
    ax4.text(0.25, lower_bound, f' Нижний ус: {lower_bound:.1f} руб.', color='mediumblue', va='center', fontweight='semibold')

    # Линии и подписи для квартилей
    ax4.axhline(q3, color='orange', linestyle=':', linewidth=1.5)
    ax4.text(0.25, q3, f' Q3: {q3:.1f} руб.', color='chocolate', va='center', fontweight='semibold')
    
    ax4.axhline(median_price, color='green', linestyle=':', linewidth=1.5)
    ax4.text(0.25, median_price, f' Медиана (Q2): {median_price:.1f} руб.', color='darkgreen', va='center', fontweight='semibold')
    
    ax4.axhline(q1, color='purple', linestyle=':', linewidth=1.5)
    ax4.text(0.25, q1, f' Q1: {q1:.1f} руб.', color='purple', va='center', fontweight='semibold')

    ax4.set_title("4. Анализ ценовых выбросов, квартилей и усов", fontweight='semibold')
    ax4.set_ylabel("Цена товара (руб.)")
    ax4.set_xlim(-0.5, 0.75)

    # Настройка зазоров между строками и колонками
    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.12, top=0.90, wspace=0.25, hspace=0.35)
    
    # ИСПРАВЛЕНИЕ: Сначала ЖЕСТКО сохраняем файл на диск, чтобы он гарантированно создался
    output_image = "task_7_charts.png"
    plt.savefig(output_image, dpi=150)
    print(f"\n[Успешно]: Графики сохранены в файл: {output_image}")
    
    # Только после сохранения открываем интерактивное окно (оно больше не заблокирует создание файла)
    plt.show()

    # ====================================================
    # КОНСОЛЬНЫЙ ВЫВОД ОТЧЕТА И АНОМАЛИЙ
    # ====================================================
    print("\n" + "="*60)
    print("АНАЛИТИЧЕСКИЙ ОТЧЕТ И РЕЗУЛЬТАТЫ ПОИСКА АНОМАЛИЙ:")
    print("="*60)
    print(f"[Метрики центра]: Средняя цена: {mean_price:.2f} руб. | Медиана: {median_price:.2f} руб.")
    print(f"[Метрики разброса]: Дисперсия: {variance_price:.2f} | Ср. отклонение: {std_dev_price:.2f} руб.")
    print(f"[Квартили]: Q1 (25%): {q1:.2f} руб. | Q3 (75%): {q3:.2f} руб. | IQR: {iqr:.2f} руб.")
    print(f"[Границы нормы]: Нижний ус: {lower_bound:.1f} руб. | Верхний ус: {upper_bound:.1f} руб.")
    print("-" * 60)
    if not anomalies.empty:
        print(f" !!! ОБНАРУЖЕНЫ СТАТИСТИЧЕСКИЕ АНОМАЛИИ В ЦЕНАХ !!!")
        print(f" - Метод IQR зафиксировал {len(anomalies)} записей ценовых выбросов.")
        print(f" - Граница математической нормы превышена для всех цен выше {upper_bound:.1f} руб.")
        print(f" - Максимальное зарегистрированное аномальное значение: {anomalies['price'].max():.2f} руб.")
    else:
        print(" - Аномалии в основном массиве цен не обнаружены.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()