#!/usr/bin/env bash

echo
echo "Buscando siguiente tutorial prioritario..."
echo

missing=$(bash scripts/check_missing_md.sh)

priority=$(echo "$missing" | grep -Ei "asprotect|armadillo|svkp|vmprotect|securom" | head -n 1)

if [ -n "$priority" ]; then
    echo "Siguiente tutorial PRIORITARIO:"
    echo
    echo "$priority"
else
    echo "No hay tutorial prioritario pendiente."
    echo
    echo "Siguiente tutorial disponible:"
    echo
    echo "$missing" | head -n 1
fi

echo
