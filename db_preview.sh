#!/data/data/com.termux/files/usr/bin/bash

DB="database/market.db"

for table in $(sqlite3 "$DB" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
do
    echo
    echo "=================================================="
    echo "TABLE : $table"
    echo "=================================================="

    sqlite3 -header -column "$DB" "SELECT * FROM \"$table\" LIMIT 5;"

done
