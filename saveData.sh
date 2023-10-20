#!bin/bash

DL_Log="/media/ponder/ADATA HM900/Log/download_log.txt"

python3 isHoliday.py
holiday=$?

if [ $holiday -eq 1 ]; then
    echo "today is Holiday , please enjoy it"
    exit 0
fi

python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"
python3 $python_script > "$DL_Log" 2>&1

result=$?
if [ $result -eq 1 ]; then
    echo "Operation Fail"
    exit 0
fi
