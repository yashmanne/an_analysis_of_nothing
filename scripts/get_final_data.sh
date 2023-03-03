#!/usr/bin/env bash

cwd=$(pwd)
echo $cwd
python ./data_tools/load_data.py $cwd
echo "Stored data under an_analysis_of_nothing/data/"
