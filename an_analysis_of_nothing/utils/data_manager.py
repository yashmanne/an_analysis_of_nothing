"""
Contains functions that count/modify original data.
"""

import pandas as pd
from collections import OrderedDict

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


def get_line_counts(data):
    """
    Get line counts for each character in the data.

    :param data: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
                 RAISE VALUE ERROR ELSE
    :return: number of lines dialogue for each unique characters
    """
    # all characters
    list_chars = data.Character.str.split(" & ").to_list()
    line_counts = {}
    # count each character's appearance
    for char_list in list_chars:
        for char in char_list:
            line_counts[char.strip()] = line_counts.get(char.strip(), 0) + 1

    # rearrange dictionary from highest to lowest
    sort_items = sorted(line_counts.items(), key=lambda x: x[1], reverse=True)
    final_counts = OrderedDict(sort_items)

    return final_counts
