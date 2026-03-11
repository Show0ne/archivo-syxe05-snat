#!/data/data/com.termux/files/usr/bin/bash

INPUT="../pdfs_sin_md.txt"
OUT="../"

while read pdf; do

name=$(basename "$pdf" .pdf)

slug=$(echo "$name" \
 | tr '[:upper:]' '[:lower:]' \
 | sed "s/[ ()]/-/g" \
 | sed "s/--*/-/g" \
 | sed "s/'//g")

md="$OUT/syxe05-$slug-reversing.md"

cat <<EOF > "$md"
# $name - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## PDF original

$name.pdf

---

## Introducción

Análisis del software **$name** desde la perspectiva de ingeniería inversa.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Análisis

Se analiza el flujo de ejecución para localizar rutinas de validación.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
EOF

echo "Generated $md"

done < "$INPUT"
