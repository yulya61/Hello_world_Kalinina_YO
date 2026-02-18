name_oper = input("Введите имя оператора:")
pressure = input("Введите текущее значение давления (Па):")
with open('sensor_log.txt', 'w', encoding='utf-8') as file:
    file.write("ОПЕРАТОР\tЗНАЧЕНИЕ\n")  # Заголовок таблицы
    file.write(f"{operator_name}\t{pressure_value}\n")
print("Данные успешно сохранены в sensor_log.txt")