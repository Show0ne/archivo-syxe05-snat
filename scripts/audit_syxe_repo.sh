#!/usr/bin/env bash

echo "======================================"
echo " SyXe'05 Archive Audit"
echo "======================================"
echo

tmp_pdf=$(mktemp)
tmp_md=$(mktemp)

echo "[+] Normalizando PDFs..."

fd -e pdf -x basename {} .pdf \
| tr '[:upper:]' '[:lower:]' \
| tr ' ' '-' \
| sed 's/[áàäâ]/a/g; s/[éèëê]/e/g; s/[íìïî]/i/g; s/[óòöô]/o/g; s/[úùüû]/u/g; s/ñ/n/g' \
| sed 's/[^a-z0-9._-]//g' \
| sed 's/\.pdf$//' \
| sed 's/-\+/-/g' \
| sort -u > "$tmp_pdf"

echo "[+] Normalizando Markdown..."

fd "syxe05-.*\.md$" reversing -x basename {} .md \
| sed 's/^syxe05-//' \
| sed 's/-reversing$//' \
| tr '[:upper:]' '[:lower:]' \
| sed 's/[áàäâ]/a/g; s/[éèëê]/e/g; s/[íìïî]/i/g; s/[óòöô]/o/g; s/[úùüû]/u/g; s/ñ/n/g' \
| sed 's/[^a-z0-9._-]//g' \
| sed 's/-\+/-/g' \
| sort -u > "$tmp_md"

echo
echo "--------------------------------------"

pdf_total=$(wc -l < "$tmp_pdf")
md_total=$(wc -l < "$tmp_md")

echo "PDFs encontrados:        $pdf_total"
echo "Markdown generados:      $md_total"

echo
echo "[+] Calculando pendientes..."

missing=$(comm -23 "$tmp_pdf" "$tmp_md")

missing_count=$(printf "%s\n" "$missing" | grep -c .)

processed=$((pdf_total - missing_count))

if [ "$pdf_total" -eq 0 ]; then
    progress=0
else
    progress=$(awk "BEGIN {printf \"%.2f\", ($processed/$pdf_total)*100}")
fi

echo
echo "--------------------------------------"

echo "Writeups procesados:     $processed"
echo "Pendientes reales:       $missing_count"
echo "Progreso real:           $progress %"

echo
echo "--------------------------------------"

if [ "$missing_count" -gt 0 ]; then
    echo "PDFs sin convertir:"
    echo
    echo "$missing"
else
    echo "✔ Todo convertido"
fi

echo
echo "======================================"

rm "$tmp_pdf" "$tmp_md"
