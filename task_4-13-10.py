array = [77, 24, 67, 52, 14, 1, 8]
n = len(array)
sum_ = 0
i = 0
while i < n:
    if i % 2 != 0:
        sum_ = sum_ + array[i]
    i = i + 1
print("Сумма элементов с нечётными индексами:", sum_)