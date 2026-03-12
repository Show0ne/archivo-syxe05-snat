#!/bin/bash

echo "Analizando repositorio..."
echo

total_pdfs=$(find . -type f -name "*.pdf" | wc -l)
generated_md=$(find reversing -type f -name "*.md" | wc -l)

pending=$((total_pdfs - generated_md))

progress=$(awk "BEGIN {printf \"%.2f\", ($generated_md/$total_pdfs)*100}")

echo "PDFs totales: $total_pdfs"
echo "Markdown generados: $generated_md"
echo "Pendientes: $pending"
echo "Progreso: $progress %"

echo
echo "--------------------------------"
echo

index_file="reversing/INDEX.md"

echo "# Reversing Writeups Index" > "$index_file"
echo >> "$index_file"

find reversing -type f -name "*.md" | sort | while read file; do

    name=$(basename "$file" .md)
    name=$(echo "$name" | tr '_' ' ')

    echo "- [$name]($file)" >> "$index_file"

done

echo
echo "Índice generado en:"
echo "$index_file"
