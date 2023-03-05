"""
Contains functions that count/modify original data.
"""
from collections import OrderedDict
import numpy as np
import pandas as pd

from . import data_constants


def load_data():
    """
    Load cleaned scripts and metadata from Google Drive.

    :return: 2 Dataframes (1 Metadata, 1 scripts).
    """
    meta = pd.read_csv(data_constants.EPISODE_LINK)

    meta.keyWords = meta.keyWords.apply(eval)
    meta.Summaries = meta.Summaries.apply(eval)

    scripts = pd.read_csv(data_constants.SCRIPTS_LINK)
    return meta, scripts


def get_line_counts(scripts):
    """
    Get line counts for each character in the data.

    :param scripts: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
                 RAISE VALUE ERROR ELSE
    :return: number of lines dialogue for each unique characters
    """
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


def get_line_counts_per_episode(scripts, characters=None):
    """
    Get line counts for main 4 characters in the data for each episode.

    :param scripts: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
                 RAISE VALUE ERROR ELSE
    :param characters: set of characters

    :return: number of lines dialogue for each unique characters
    """
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
