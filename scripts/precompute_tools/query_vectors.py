"""
Contains functions to precompute vectors for cosine similarity
for episode search.
"""
import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch


def create_corpus_embeddings(df_script):
    """
    Use sentence transformer to generate dialogue embeddings
    for episode querying and store sharded files as numpy arrays.
    NOTE: Takes 8 minutes to run.
    :param df_script: The scripts DataFrame.
            Must have Dialogue column.
    :return: None
    """
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    corpus = df_script.Dialogue.values
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    tensors = torch.split(corpus_embeddings, split_size_or_sections=5459)

    curr_path = os.getcwd()
    base_pth = curr_path.split("an_analysis_of_nothing", maxsplit=1)[0]
    data_dir = base_pth + \
        'an_analysis_of_nothing/an_analysis_of_nothing/static/data'
    for i, tensor in enumerate(tensors):
        np.save(f"{data_dir}/dialogue_tensors/tensor_{i}.npy",
                tensor.numpy())
    return
