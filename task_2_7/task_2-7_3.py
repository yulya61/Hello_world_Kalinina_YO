seq = ["ATATACGCGTA", "CTTCGGNGGA"]
for sequence in seq:
    print("\nПоследовательность целиком:")
    print(sequence)
    
    print("Та же последовательность, но по символам:")
    # Перебираем каждый символ в последовательности
    for nucleotide in sequence:
        print(nucleotide)
    
    print("---")

print("Цикл выполнен")