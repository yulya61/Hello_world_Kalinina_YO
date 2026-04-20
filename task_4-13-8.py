array = [77, 24, -67, 52, -14, 1, 8]
n = len(array)
i = 0
count = 0

while i < n:
    if array[i] > 0:
        count = count + 1
    i = i + 1

print("Количество положительных чисел в массиве:", count)