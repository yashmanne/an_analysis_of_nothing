"""
Script to download cleaned data into analysis_of_nothing/data/
"""
import os
import pandas as pd
from data_tools import load_data

if __name__ == "__main__":
    cwd = os.getcwd()
    base_path = cwd.split("an_analysis_of_nothing", maxsplit=1)[0]
    data_folder = base_path + 'an_analysis_of_nothing/data/'
    meta_name = data_folder + 'metadata.csv'
    script_name = data_folder + 'scripts.csv'
    meta, scripts = load_data.get_final_data()
    meta.to_csv(meta_name, index=False)
    scripts.to_csv(script_name, index=False)
    print('Done saving data to an_analysis_of_nothing/data/')
