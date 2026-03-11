#!/usr/bin/env bash

echo "Buscando PDFs sin Markdown..."
echo

fd -e pdf . | while read -r pdf; do

    name=$(basename "$pdf" .pdf)

    slug=$(echo "$name" \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/[^a-z0-9]/-/g')

    md="reversing/software/syxe05-${slug}-reversing.md"

    if [ ! -f "$md" ]; then
        echo "$pdf"
    fi

done
