"""
Contains functions that count/modify original data.
"""

import pandas as pd
from collections import OrderedDict


def get_line_counts(data):
    """
    :param: data: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
    :return: number of lines dialogue for each unique characters
    """
    # all characters
    list_chars = data.Character.str.split(" & ").to_list()
    line_counts = {}
    # count each character's apperance
    for char_list in list_chars:
        for char in char_list:
            line_counts[char.strip()] = line_counts.get(char.strip(), 0) + 1

    # rearrange dictionary from highest to lowest
    sort_items = sorted(line_counts.items(), key=lambda x: x[1], reverse=True)
    final_counts = OrderedDict(sort_items)

    return final_counts