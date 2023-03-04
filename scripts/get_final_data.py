"""
Script to download cleaned data into analysis_of_nothing/data/
Prerequisite: Activate conda environment with:
    conda activate nothing
"""
import os
import pandas as pd
import text2emotion as te
from tqdm.auto import tqdm

from data_tools import load_data
from sentiment_tools import sentiment

if __name__ == "__main__":
    cwd = os.getcwd()
    base_path = cwd.split("an_analysis_of_nothing", maxsplit=1)[0]
    data_folder = base_path + 'an_analysis_of_nothing/data/'
    meta_name = data_folder + 'metadata.csv'
    script_name = data_folder + 'scripts.csv'
    meta, scripts = load_data.get_final_data()
    print("Done gathering cleaned data.")
    print("Now running text2emotion...")
    scripts = sentiment.get_emotions(scripts)
    print("Done gathering emotions.")
    meta.to_csv(meta_name, index=False)
    scripts.to_csv(script_name, index=False)
    print('Done saving data to an_analysis_of_nothing/data/')
