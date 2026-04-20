n = int(input("Введите количество чисел N: "))
first_number = float(input("Введите число 1: "))
max_value = first_number
i = 2
while i <= n:
    x = float(input(f"Введите число {i}: "))
    if x > max_value:
        max_value = x
    i = i + 1
print("Максимальное из введённых чисел:", max_value)