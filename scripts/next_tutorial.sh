#!/usr/bin/env bash

echo
echo "Buscando siguiente tutorial prioritario..."
echo

missing=$(bash scripts/check_missing_md.sh | grep -v -i "calls_a_reparar")

priority=$(echo "$missing" | grep -Ei "asprotect|armadillo|svkp|vmprotect|themida|securom")

if [ -n "$priority" ]; then
    echo "Siguiente tutorial PRIORITARIO:"
    echo
    echo "$priority" | head -n 1
else
    echo "No hay tutorial prioritario pendiente."
    echo
    echo "Siguiente tutorial disponible:"
    echo
    echo "$missing" | head -n 1
fi

echo
