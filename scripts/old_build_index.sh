#!/bin/bash

echo "Analizando repositorio..."
echo

# Contar PDFs
total_pdfs=$(find . -type f -name "*.pdf" | wc -l)

# Contar Markdown
generated_md=$(find . -type f -name "*.md" | wc -l)

# Calcular pendientes
pending=$((total_pdfs - generated_md))

# Calcular progreso
progress=$(awk "BEGIN {printf \"%.2f\", ($generated_md/$total_pdfs)*100}")

echo "PDFs totales: $total_pdfs"
echo "Markdown generados: $generated_md"
echo "Pendientes: $pending"
echo "Progreso: $progress %"

echo
echo "--------------------------------"

# Milestone 50%
half=$((total_pdfs / 2))
remaining_for_half=$((half - generated_md))

echo "Milestone 50%:"
echo "Writeups necesarios para 50%: $half"

if [ $generated_md -lt $half ]; then
    echo "Faltan para llegar al 50%: $remaining_for_half"
else
    echo "✔ Ya se superó el 50%"
fi

echo
echo "Generando índice..."
echo

# Generar índice simple
index_file="reversing/INDEX.md"

echo "# Reversing Writeups Index" > $index_file
echo >> $index_file

find reversing -type f -name "*.md" | sort | while read file; do
    name=$(basename "$file")
    echo "- [$name]($file)" >> $index_file
done

echo
echo "Índice generado en:"
echo "$index_file"
