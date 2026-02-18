medium_name = input("Введите название питательной среды: ")
agar_concentration = float(input("Введите концентрацию агара (%): "))
sterilization_temp = float(input("Введите температуру стерилизации: "))

with open('recipe.txt', 'w', encoding='utf-8') as file:
    file.write(medium_name + "\n")
    file.write("Параметры:\n")
    file.write("  - Концентрация агара: " + str(agar_concentration) + " %\n")
    file.write("  - Температура стерилизации: " + str(sterilization_temp) + " °C\n")

print("Файл 'recipe.txt' успешно сформирован!")