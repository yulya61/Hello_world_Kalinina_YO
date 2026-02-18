volume = int(input("Введите объём раствора (в мл): "))
salt_mass = volume * 0.009
with open(r"C:\Users\Юлия\AppData\Local\Programs\Microsoft VS Code\recipe.txt", "w", encoding="utf-8") as file:
    file.write(f"ОТЧЁТ ПО ПРИГОТОВЛЕНИЮ: \n")
    file.write("-" * 23)
    file.write(f"\nОбщий объём: {volume} мл\nМасса соли: {salt_mass:.2f} г\nОбъём воды: {volume} мл")