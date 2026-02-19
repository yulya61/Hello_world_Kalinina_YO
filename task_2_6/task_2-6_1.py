pH = float(input("Введите значение pH: "))
if pH < 7.0:
    print(f"pH = {pH} — это кислая среда")
elif pH > 7.0:
    print(f"pH = {pH} — это щелочная среда")
else:
    print(f"pH = {pH} — это нейтральная среда")
    