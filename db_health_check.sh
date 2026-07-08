#!/data/data/com.termux/files/usr/bin/bash

DB="database/market.db"

echo "=================================================="
echo "GREEN BULL DATABASE HEALTH CHECK"
echo "=================================================="

if [ ! -f "$DB" ]; then
    echo "Database not found: $DB"
    exit 1
fi

echo
echo "DATABASE FILE"
ls -lh "$DB"

echo
echo "INTEGRITY CHECK"
sqlite3 "$DB" "PRAGMA integrity_check;"

echo
echo "FOREIGN KEY CHECK"
sqlite3 "$DB" "PRAGMA foreign_key_check;"

echo
echo "DATABASE SIZE"
sqlite3 "$DB" "
SELECT
page_count,
page_size,
ROUND(page_count*page_size/1024.0/1024.0,2)||' MB'
FROM pragma_page_count(), pragma_page_size();
"

echo
echo "=================================================="
echo "TABLE LIST"
echo "=================================================="

sqlite3 "$DB" "
SELECT name
FROM sqlite_master
WHERE type='table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name;
"

echo
echo "=================================================="
echo "ROW COUNT"
echo "=================================================="

for table in $(sqlite3 "$DB" "
SELECT name
FROM sqlite_master
WHERE type='table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name;
")
do
    rows=$(sqlite3 "$DB" "SELECT COUNT(*) FROM \"$table\";" 2>/dev/null)
    printf "%-35s %12s\n" "$table" "$rows"
done

echo
echo "=================================================="
echo "INDEXES"
echo "=================================================="

sqlite3 "$DB" "
SELECT name,tbl_name
FROM sqlite_master
WHERE type='index'
ORDER BY tbl_name,name;
"

echo
echo "=================================================="
echo "UPDATE LOG"
echo "=================================================="

sqlite3 "$DB" "
SELECT *
FROM update_log
ORDER BY last_run DESC
LIMIT 10;
"

echo
echo "=================================================="
echo "HISTORICAL DATA RANGE"
echo "=================================================="

sqlite3 "$DB" "
SELECT
MIN(date),
MAX(date),
COUNT(*)
FROM historical_data;
"

echo
echo "=================================================="
echo "SYMBOL COVERAGE"
echo "=================================================="

sqlite3 "$DB" "
SELECT
(SELECT COUNT(*) FROM stock_master),
(SELECT COUNT(*) FROM historical_data),
(SELECT COUNT(DISTINCT symbol) FROM historical_data),
(SELECT COUNT(*) FROM fundamental_data),
(SELECT COUNT(DISTINCT symbol) FROM fundamental_data);
"

echo
echo "=================================================="
echo "TOP 20 TABLES"
echo "=================================================="

for table in $(sqlite3 "$DB" "
SELECT name
FROM sqlite_master
WHERE type='table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name;
")
do
    echo
    echo "----- $table -----"
    sqlite3 "$DB" "PRAGMA table_info($table);"
done

echo
echo "=================================================="
echo "CHECK COMPLETE"
echo "=================================================="
