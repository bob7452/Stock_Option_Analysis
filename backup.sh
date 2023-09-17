#!/bin/bash

today=$(date +"%Y-%m-%d")
op_dir="/media/ponder/ADATA HM900/OptionData"
stock_dir="/media/ponder/ADATA HM900/StockPriceData"
target_file="/media/ponder/ADATA HM900/BackUp/$today.tar.gz"

tar -czvf "$target_file" "$stock_dir" "$op_dir"

if [ $? -eq 0 ]; then
    echo "success：$target_file"
else
    echo "fail"
    exit 1
fi
