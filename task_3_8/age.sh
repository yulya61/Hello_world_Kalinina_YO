#!/bin/bash
# Присваивание
CURRENT_YEAR=2026
BIRTH_YEAR=2000

# Вычисление (Арифметика) - ИСПРАВЛЕНО!
AGE=$((CURRENT_YEAR - BIRTH_YEAR))

# Вывод с интерполяцией
echo "Текущий год: $CURRENT_YEAR"
echo "Ваш примерный возраст: $AGE"

