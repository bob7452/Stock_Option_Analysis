#!/bin/bash

op_dir="/media/ponder/Disk_D/OptionData"
stock_dir="/media/ponder/Disk_D/StockPriceData"
target_file="/media/ponder/Disk_D/BackUp/data.tar.gz"
google_dir="/home/ponder/migoogledrive/Stock"


tmp_dir="/tmp/backup_temp"
mkdir -p "$tmp_dir"

cp -r "$stock_dir" "$tmp_dir"
cp -r "$op_dir" "$tmp_dir"

tar -czvf "$target_file" -C "$tmp_dir" .

rm -r "$tmp_dir"

if [ $? -eq 0 ]; then
    echo "success：$target_file"
else
    echo "fail"
    exit 1
fi

cp "$target_file" "$google_dir"

if [ $? -eq 0 ]; then
    echo "success：$target_file move to $google_dir"
else
    echo "fail"
    exit 1
fi

