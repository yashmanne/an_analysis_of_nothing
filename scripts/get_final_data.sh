#!/usr/bin/env bash

cwd=$(pwd)
echo $cwd
conda activate nothing
python ./get_final_data.py
echo "Stored data under an_analysis_of_nothing/data/"
conda deactivate nothing
