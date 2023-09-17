#!/bin/bash

python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"
python3 $python_script
git clean -df

current_date=$(date +"%Y-%m-%d")
op_dir="/media/ponder/ADATA HM900/OptionData" 
stock_dir= "/media/ponder/ADATA HM900/StockPriceData"
target_directory="/media/ponder/ADATA HM900/BackUp/$current_date" 


if [ -d "$target_directory" ]; then
    mkdir -p "$target_directory"
fi

cp -r "$op_dir" "$target_directory"

if [ $? -eq 0 ]; then
    echo "op data copy success"
else
    echo "op data copy fail"
    exit 1
fi

cp -r "$stock_dir" "$target_directory"

if [ $? -eq 0 ]; then
    echo "stock data copy success"
else
    echo "stock data copy fail"
    exit 1
fi

pyscript"/home/ponder/Stock_Option_Analysis/optionCal.py"
python3 $pyscript
git clean -df
