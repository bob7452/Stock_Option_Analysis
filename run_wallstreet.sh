#!/bin/bash

#set -e

DL_Log="/media/ponder/Disk_D/Log/download_log.txt"
op_Log="/media/ponder/Disk_D/Log/option_cal.txt"
daily_Log="/media/ponder/Disk_D/Log/daily_log.txt"


python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"
python3 $python_script > "$DL_Log" 2>&1

result=$?
if [ $result -eq 1 ]; then
    echo "Operation Fail"
    exit 0
fi

git clean -df

pyscript="/home/ponder/Stock_Option_Analysis/optionCal.py"
python3 $pyscript > "$op_Log" 2>&1

result=$?
if [ $result -eq 1 ]; then
    echo "Operation Fail"
    exit 0
fi

git clean -df

pyscript="/home/ponder/Stock_Option_Analysis/dailyReport.py"
python3 $pyscript > "$daily_Log" 2>&1

result=$?
if [ $result -eq 1 ]; then
    echo "Operation Fail"
    exit 0
fi

git clean -df
