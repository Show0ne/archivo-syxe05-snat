#!/usr/bin/env bash

echo "Buscando PDFs sin Markdown..."
echo

find . -type f -iname "*.pdf" | while read pdf; do

    name=$(basename "$pdf")

    base=$(echo "$name" \
        | sed 's/\.pdf$//' \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/[ ()]/-/g' \
        | sed 's/--*/-/g')

    md="reversing/software/syxe05-${base}-reversing.md"

    if [ ! -f "$md" ]; then
        echo "$pdf"
    fi

done
