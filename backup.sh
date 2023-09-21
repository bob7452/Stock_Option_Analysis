#!/bin/bash

today=$(date +"%Y-%m-%d")
op_dir="/media/ponder/ADATA HM900/OptionData"
stock_dir="/media/ponder/ADATA HM900/StockPriceData"
target_file="/media/ponder/ADATA HM900/BackUp/$today.tar.gz"
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

