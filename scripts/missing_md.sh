#!/usr/bin/env bash

echo "Buscando PDFs sin Markdown..."
echo

fd -e pdf -0 | while IFS= read -r -d '' pdf; do

    base=$(basename "$pdf" .pdf)

    slug=$(echo "$base" \
        | tr '[:upper:]' '[:lower:]' \
        | tr ' ' '-' \
        | sed 's/[áàäâ]/a/g; s/[éèëê]/e/g; s/[íìïî]/i/g; s/[óòöô]/o/g; s/[úùüû]/u/g; s/ñ/n/g' \
        | sed 's/[^a-z0-9._-]//g')

    md="reversing/software/syxe05-${slug}-reversing.md"

    if [ ! -f "$md" ]; then
        echo "$pdf"
    fi

done
