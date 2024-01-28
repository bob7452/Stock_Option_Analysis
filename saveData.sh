#!bin/bash

DL_Log="/media/ponder/Disk_D/Log/download_log.txt"


python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"
python3 $python_script > "$DL_Log" 2>&1

result=$?
if [ $result -eq 1 ]; then
    echo "Operation Fail"
    exit 0
fi
