n = int(input("Введите N: "))
sum_ = 1
i = 1
while i <= n:
    sq = i ** 2
    sum_ = sum_ + sq
    i = i + 1
print("Сумма квадратов первых", n, "натуральных чисел:", sum_)