"""
Script to download cleaned data into analysis_of_nothing/data/
Prerequisite: Activate conda environment with:
    conda activate nothing
"""
import os
import numpy as np
import pandas as pd

from data_tools import load_data
from precompute_tools import sentiment, query_vectors

if __name__ == "__main__":
    cwd = os.getcwd()
    base_path = cwd.split("an_analysis_of_nothing", maxsplit=1)[0]
    data_folder = base_path + \
        'an_analysis_of_nothing/an_analysis_of_nothing/static/data/'
    if not os.path.exists(data_folder):
        os.mkdirs(data_folder)
    meta_name = data_folder + 'metadata.csv'
    script_name = data_folder + 'scripts.csv'
    meta, scripts = load_data.get_final_data()
    print("Done gathering cleaned data.")
    print("Now running text2emotion...")
    scripts = sentiment.get_emotions(scripts)
    print("Done gathering emotions.")
    meta.to_csv(meta_name, index=False)
    scripts.to_csv(script_name, index=False)
    print(f'Done saving data to {data_folder}')
    print("Now precomputing search query vectors...")
    query_vectors.create_corpus_embeddings(df_script=scripts)
    print("Done saving precomputed search query vectors.")

