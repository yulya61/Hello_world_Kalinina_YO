#!/bin/bash
echo "Введите вашу массу тела (в кг):"
read WEIGHT
echo "Введите ваш рост (в метрах, например 1.75):"
read HEIGHT
BMI=$(echo "$WEIGHT / ($HEIGHT * $HEIGHT)" | bc | awk '{printf("%d\n", $1)}')
echo "=============================="
echo "Ваш индекс массы тела (ИМТ): $BMI"
echo "=============================="
