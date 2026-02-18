weight = float(input("Введите  ваш вес (кг): "))
height_cm = float(input("Введите ваш рост (м): "))
height_m = height_cm / 100
bmi = weight / (height_m ** 2)

print("\n--- Отчет о состоянии здоровья ---")
print(f"Рост:\t\t{height_cm} см")
print(f"Вес:\t\t{weight} кг")
print(f"Индекс массы тела:\t{bmi:.2f}")