donor = input("Введите группу крови донора (I, II, III, IV): ").strip().upper()
recipient = input("Введите группу крови реципиента (I, II, III, IV): ").strip().upper()
valid_groups = {"I", "II", "III", "IV"}

if donor not in valid_groups or recipient not in valid_groups:
    print("Ошибка: такой группы крови не существует")
else:
    if donor == "I" or donor == recipient or (donor == "II" and recipient == "IV") or (donor == "III" and recipient == "IV"):
        print(f"Кровь донора группы {donor} можно переливать реципиенту с группой {recipient}")
    else:
        print(f"Кровь донора группы {donor} НЕЛЬЗЯ переливать реципиенту с группой {recipient}")