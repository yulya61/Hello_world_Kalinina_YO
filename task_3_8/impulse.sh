#!/bin/bash
if [ $# -ne 2 ]; then
    echo "Ошибка: недостаточно данных!"
    echo "Использование: ./impulse.sh <имя_гена> <уровень_экспрессии>"
    exit 1
fi
GENE_NAME=$1
EXPRESSION_LEVEL=$2
echo "Экспрессия гена $GENE_NAME составляет $EXPRESSION_LEVEL единиц"
