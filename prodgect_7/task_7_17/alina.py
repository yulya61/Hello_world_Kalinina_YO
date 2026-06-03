import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

try:
    connection = psycopg2.connect(
         host="localhost",
         port="5434",
         user="postgres",
         password="student",
         database="student_task" 
    )
    print("✓ Подключение установлено")

    df_products = pd.read_sql("""
        SELECT
            p.name AS product,
            ROUND(AVG(pr.price)::numeric, 2) AS avg_price,
            COUNT(pr.id) AS total_offers,
            MIN(pr.price) AS min_price,
            MAX(pr.price) AS max_price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        GROUP BY p.name
        ORDER BY avg_price DESC
    """, connection)

    df_all_prices = pd.read_sql("SELECT price FROM prices", connection)

    df_missing = pd.read_sql("""
        SELECT
            p.name AS product
        FROM products p
        LEFT JOIN prices pr ON p.id = pr.product_id
        WHERE pr.id IS NULL
        ORDER BY p.name
    """, connection)

    print(f"Продуктов в выборке:           {len(df_products)}")
    print(f"Всего записей о ценах:         {len(df_all_prices)}")
    print(f"Продуктов без цен (аномалия):  {len(df_missing)}")

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    connection.close()
    print("✓ Соединение закрыто\n")

# -------------------------------------------------------------------------
# БЛОК 2: ПОДГОТОВКА ДАННЫХ
# -------------------------------------------------------------------------

df_products["short_name"] = df_products["product"].apply(
    lambda x: x[:12] + "..." if len(x) > 12 else x
)

PRICE_THRESHOLD = df_products["avg_price"].quantile(0.75)
overall_avg_price = df_products["avg_price"].mean()

bar_colors = [
    "#d9534f" if p > PRICE_THRESHOLD else "#4a90d9"
    for p in df_products["avg_price"]
]

# -------------------------------------------------------------------------
# БЛОК 3: ПОСТРОЕНИЕ ГРАФИКОВ
# -------------------------------------------------------------------------

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})

fig = plt.figure(figsize=(16, 10))
fig.suptitle("Анализ цен на продукты", fontsize=15, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(2, 1, figure=fig, height_ratios=[5, 4], hspace=0.45)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# -- ГРАФИК 1: Средняя цена по продуктам --
bars1 = ax1.barh(
    df_products["short_name"],
    df_products["avg_price"],
    color=bar_colors,
    edgecolor="white",
    height=0.6,
)

for bar, val in zip(bars1, df_products["avg_price"]):
    ax1.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.2f} ₽",
        va="center",
        fontsize=9,
    )

ax1.axvline(
    overall_avg_price,
    color="darkorange",
    linestyle="--",
    linewidth=1.3,
    label=f"Среднее: {overall_avg_price:.2f} ₽"
)

ax1.set_xlabel("Средняя цена (₽)")
ax1.set_title("Средняя цена по продуктам", fontweight="bold", pad=8)

legend_patches = [
    Patch(facecolor="#4a90d9", label=f"Норма (≤ {PRICE_THRESHOLD:.0f} ₽)"),
    Patch(facecolor="#d9534f", label="Высокая цена"),
]
ax1.legend(handles=legend_patches, fontsize=8, loc="lower right")

# -- ГРАФИК 2: Распределение цен --
price_counts = df_all_prices["price"].dropna()

ax2.hist(
    price_counts,
    bins=20,
    color="#f0ad4e",
    edgecolor="white"
)

median_price = price_counts.median()
mean_price = price_counts.mean()
std_price = price_counts.std()

ax2.axvline(
    median_price,
    color="crimson",
    linestyle="--",
    linewidth=1.5,
    label=f"Медиана: {median_price:.2f} ₽"
)
ax2.axvline(
    mean_price,


color="darkblue",
    linestyle=":",
    linewidth=1.5,
    label=f"Среднее: {mean_price:.2f} ₽"
)

ax2.set_xlabel("Цена (₽)")
ax2.set_ylabel("Количество записей")
ax2.set_title("Распределение цен", fontweight="bold", pad=8)
ax2.legend(fontsize=8)

stats_text = (
    f"Всего цен: {len(price_counts)}\n"
    f"Среднее: {mean_price:.2f} ₽\n"
    f"Медиана: {median_price:.2f} ₽\n"
    f"Ст. откл.: {std_price:.2f} ₽"
)

ax2.text(
    0.97, 0.95, stats_text,
    transform=ax2.transAxes,
    va="top",
    ha="right",
    fontsize=8,
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "lightyellow",
        "edgecolor": "lightgray",
        "alpha": 0.8
    }
)

# Аномалии
if len(df_missing) > 0:
    fig.text(
        0.5, -0.03,
        f"Аномалия: {len(df_missing)} продуктов без цен: {', '.join(df_missing['product'].head(3))}"
        + ("..." if len(df_missing) > 3 else ""),
        ha="center",
        fontsize=9,
        color="#8b0000",
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "#fff3f3",
            "edgecolor": "#d9534f"
        }
    )
else:
    fig.text(
        0.5, -0.03,
        "Аномалий не обнаружено",
        ha="center",
        fontsize=9,
        color="#2e7d32",
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "#e8f5e9",
            "edgecolor": "#4caf50"
        }
    )

# -------------------------------------------------------------------------
# БЛОК 4: СОХРАНЕНИЕ
# -------------------------------------------------------------------------

OUTPUT_FILE = "price_analysis.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"График сохранён: {OUTPUT_FILE}")
plt.show()



