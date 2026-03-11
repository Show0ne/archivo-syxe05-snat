#!/usr/bin/env bash

# ======================================
# SyXe Archive – Next PDF helper
# ======================================

tmp_pdf=$(mktemp)
tmp_md=$(mktemp)

# Normalizar PDFs
fd -e pdf | while read -r pdf; do
    base=$(basename "$pdf" .pdf | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
    echo "$base|$pdf"
done | sort -u > "$tmp_pdf"

# Normalizar markdown existentes
fd "syxe05-.*\.md$" reversing | while read -r md; do
    base=$(basename "$md" .md)
    base=${base#syxe05-}
    base=${base%-reversing}
    base=$(echo "$base" | tr '[:upper:]' '[:lower:]')
    echo "$base"
done | sort -u > "$tmp_md"

# Buscar el primer PDF pendiente
while IFS="|" read -r base path; do
    if ! grep -qx "$base" "$tmp_md"; then
        echo "$path"
        rm "$tmp_pdf" "$tmp_md"
        exit 0
    fi
done < "$tmp_pdf"

echo "✔ Todos los PDFs ya tienen markdown"

rm "$tmp_pdf" "$tmp_md"
