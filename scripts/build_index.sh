#!/usr/bin/env bash

repo_root="."
md_dir="reversing/software"
index_file="reversing/INDEX.md"

echo "Analizando repositorio..."

total_pdf=$(find "$repo_root" -type f -iname "*.pdf" | wc -l)
total_md=$(find "$md_dir" -type f -iname "*.md" | wc -l)

pending=$((total_pdf-total_md))

progress=$(awk "BEGIN {printf \"%.2f\", ($total_md/$total_pdf)*100}")

echo
echo "PDFs totales: $total_pdf"
echo "Markdown generados: $total_md"
echo "Pendientes: $pending"
echo "Progreso: $progress %"
echo

echo "Generando índice..."

mkdir -p reversing

cat > "$index_file" <<EOF
# Archivo SyXe'05 – Reversing Tutorials

Repositorio de tutoriales de ingeniería inversa publicados por **SyXe'05** y miembros de **SNAT**.

## Estadísticas

- PDFs totales: $total_pdf
- Markdown generados: $total_md
- Pendientes: $pending
- Progreso: $progress %

---

## Tutoriales disponibles

EOF

ls "$md_dir" | sort | while read file; do
    name=$(echo "$file" \
        | sed 's/syxe05-//' \
        | sed 's/-reversing.md//' \
        | sed 's/-/ /g')

    echo "- [$name]($md_dir/$file)" >> "$index_file"
done

echo
echo "Índice generado en:"
echo "$index_file"
