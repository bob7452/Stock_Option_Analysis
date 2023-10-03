#!/bin/bash

DL_Log="/media/ponder/ADATA HM900/Log/download_log.txt"
op_Log="/media/ponder/ADATA HM900/Log/opcal_log.txt"
daily_Log="/media/ponder/ADATA HM900/Log/daily_log.txt"

python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"
python3 $python_script > "$DL_Log" 2>&1
git clean -df

pyscript="/home/ponder/Stock_Option_Analysis/optionCal.py"
python3 $pyscript 2> "$op_Log" 2>&1
git clean -df

pyscript="/home/ponder/Stock_Option_Analysis/dailyReport.py"
python3 $pyscript 2> "$daily_Log" 2>&1
git clean -df
