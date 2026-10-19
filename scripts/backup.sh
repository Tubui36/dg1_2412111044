#!/bin/bash
# Su dung: ./backup.sh <thu_muc_can_sao_luu>

if [ $# -ne 1 ] || [ ! -d "$1" ]; then
    echo "Cach dung: $0 <thu_muc_can_sao_luu>" >&2
    exit 1
fi

SRC=$(realpath "$1")
NAME=$(basename "$SRC")
DEST_DIR="$HOME/backup"
LOG="$HOME/dg1_2412111044/logs/backup.log"
FILE="$DEST_DIR/${NAME}_$(date +%Y%m%d_%H%M%S).tar.gz"

mkdir -p "$DEST_DIR"

if tar -czf "$FILE" -C "$(dirname "$SRC")" "$NAME"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') $FILE" >> "$LOG"
    echo "Da sao luu: $FILE"
else
    echo "Sao luu that bai" >&2
    exit 2
fi
