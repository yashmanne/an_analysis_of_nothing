#!/usr/bin/env bash

cwd=$(pwd)
echo $cwd
python ./get_final_data.py
echo "Stored data under an_analysis_of_nothing/data/"
