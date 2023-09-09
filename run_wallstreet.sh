#!/bin/bash

python_script="/home/ponder/Stock_Option_Analysis/wallstreetTest.py"

day_of_week=$(date +%u)
hour_of_day=$(date +%H)

if [ $day_of_week -ge 2 -a $day_of_week -le 6 -a $hour_of_day -eq 9 ]; then
    python3 $python_script

    git clean -df
fi

