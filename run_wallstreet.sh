#!/bin/bash

python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"
python3 $python_script
git clean -df

pyscript="/home/ponder/Stock_Option_Analysis/optionCal.py"
python3 $pyscript
git clean -df

pyscript="/home/ponder/Stock_Option_Analysis/dailyReport.py"
python3 $pyscript
git clena -df
