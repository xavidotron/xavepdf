#!/bin/bash

o="$(echo "$1" | cut -d . -f 1)-mod.pdf"

qpdf -qdf "$1" "$o"
LANG=C sed -i '' 's/re f/re/' "$o"
