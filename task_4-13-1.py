A = float(input("Введите число A: "))
B = float(input("Введите число B: "))
C = float(input("Введите число C: "))
D = float(input("Введите число D: "))
min_value = A

if B < min_value:
    min_value = B

if C < min_value:
    min_value = C

if D < min_value:
    min_value = D

print("Минимальное из введённых чисел:", min_value)