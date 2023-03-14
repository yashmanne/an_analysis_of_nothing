# Overview

This folder contains the scripts used to clean the raw data as well as some additional precomputing. Note that these functions are **omitted from test coverage** due to a vast amount of manual research for cleaning as well as the fact that this script should only be run once without any edits.

* `./data_tools/`: Contains functions for data cleaning and integration of data sources from raw script data and IMDb metadata across multiple source.
  * This includes accounting for episode numbering mismatches, removing typos for `Character`/`Director` fields, and more. 
* `./precompute_tools/`: Contains functions for precomputing emotional distribution of each line of dialogue as well as the code for generating the feature vectors for subsequent cosine similarity tasks as part of episode querying. 
  * Note that these feature vectors are pre-trained BERT embeddings for each line of dialogue.
* `./get_final_data.py`: Executes all data cleaning & precomputing code.
  * Outputs: 
    * Cleaned Metadata: `../an_analysis_of_nothing/static/data/metadata.csv`
    * Cleaned Scripts With Emotions: `../an_analysis_of_nothing/static/data/scripts.csv`
    * Sharded Feature Vectors: `../an_analysis_of_nothing/static/data/dialogue_tensors/tensor_*.npy`
LINK EXAMPLEHERERE ERE
