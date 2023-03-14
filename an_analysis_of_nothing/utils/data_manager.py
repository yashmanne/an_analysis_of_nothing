from collections import OrderedDict
from typing import Tuple, List, Optional
import numpy as np
import pandas as pd
import torch

from . import data_constants


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load cleaned scripts and metadata from Google Drive.

    :return: 2 Dataframes (1 Metadata, 1 scripts).
    """
    meta = pd.read_csv(data_constants.EPISODE_LINK)

    meta.keyWords = meta.keyWords.apply(eval)
    meta.Summaries = meta.Summaries.apply(eval)

    scripts = pd.read_csv(data_constants.SCRIPTS_LINK)
    return meta, scripts


def get_episode_query_tensors(num_shards: int = 10) -> torch.Tensor:
    """
    Load in pre-computed feature vectors for cosine similarity.

    :param num_shards: number of times the raw feature vector
                       was sharded to allow Git tracking.
    """
    if not isinstance(num_shards, int):
        raise TypeError("num_shards must be an integer")
    all_tensors = []
    for i in range(num_shards):
        npy_tensor = np.load(f"./static/data/dialogue_tensors/tensor_{i}.npy")
        all_tensors.append(npy_tensor)
    npy_2d = np.concatenate(all_tensors)
    torch_tensor = torch.from_numpy(npy_2d)
    return torch_tensor


def get_line_counts(scripts: pd.DataFrame) -> OrderedDict:
    """
    Get line counts for each character in the data.

    :param scripts: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
    :return: number of lines dialogue for each unique characters
    """
    if not isinstance(scripts, pd.DataFrame):
        raise TypeError("scripts must be an pd.DataFrame")

    # all characters
    list_chars = scripts.Character.str.split(" & ").to_list()
    line_counts = {}
    # count each character's appearance
    for char_list in list_chars:
        for char in char_list:
            line_counts[char.strip()] = line_counts.get(char.strip(), 0) + 1

    # rearrange dictionary from highest to lowest
    sort_items = sorted(line_counts.items(), key=lambda x: x[1], reverse=True)
    final_counts = OrderedDict(sort_items)

    return final_counts


def get_line_counts_per_episode(
        scripts: pd.DataFrame,
        characters: Optional[List[str]] = None) -> OrderedDict:
    """
    Get line counts for main 4 characters in the data for each episode.

    :param scripts: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
    :param characters: set of characters, defaults to
        {'JERRY', 'GEORGE', 'ELAINE', 'KRAMER'}
    :raise TypeError: if scripts is not a
        Pandas DataFrame or if characters is not a set or None

    :return: number of lines dialogue for each unique characters
    """
    if not isinstance(scripts, pd.DataFrame):
        raise TypeError("Input scripts must be a Pandas DataFrame")

    if characters is not None and not isinstance(characters, list):
        raise TypeError("Input characters must be a list or None")

    if characters is None:
        characters = {'JERRY', 'GEORGE', 'ELAINE', 'KRAMER'}

    seid_to_id = dict(zip(
        sorted(scripts.SEID.unique()),
        np.arange(len(scripts.SEID.unique()))
    ))
    # all characters
    list_chars = scripts.Character.str.split(" & ").to_list()
    line_counts = OrderedDict.fromkeys(characters, None)
    for char in line_counts:
        line_counts[char] = np.zeros(len(seid_to_id))
    # count each character's appearance
    for i, char_list in enumerate(list_chars):
        seid_id = seid_to_id[scripts.SEID.values[i]]
        for char in char_list:
            # update counts of tracked characters
            if char.strip() in line_counts:
                line_counts[char.strip()][seid_id] += 1

    return line_counts
