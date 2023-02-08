"""
Contains functions to load data from online sources.
"""
import numpy as np
import pandas as pd

from . import data_constants

def read_scripts():
    """
    Read in `Seinfeld Chronicles` script data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    df = pd.read_csv(data_constants.SCRIPTS_LINK)
    df.drop(columns = df.columns[0], inplace=True)
    df = df.astype({
            'Season': int,
            'EpisodeNo': int
        }
    )
    return df

def read_episode_info():
    """
    Read in `Seinfeld Chronicles` episode data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    df = pd.read_csv(data_constants.EPISODE_LINK)
    df.drop(columns=df.columns[0], inplace=True)
    df = df.astype({
            'Season': int,
            'EpisodeNo': int
        }
    )
    return df

def read_imdb_metadata():
    """
    Read in `Seinfeld Chronicles` episode data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    seinfeld_id = data_constants.SEINFELD_PARENT_TCONST

    # Gather all episode metadata
    all_eps = pd.read_csv(data_constants.IMDB_EPISODE, delimiter='\t')
    all_eps = all_eps[all_eps.parentTconst == seinfeld_id]
    epi_ids = set(all_eps['tconst'].values)

    # Gather all rating data
    ratings = pd.read_csv(data_constants.IMDB_RATING, delimiter='\t')
    ratings = ratings[ratings.tconst.isin(epi_ids)]

    # Gather additional metadata
    basics = pd.read_csv(data_constants.IMDB_BASICS, delimiter='\t',
        usecols=['tconst', 'originalTitle', 'runtimeMinutes']
    )
    basics = basics[basics.tconst.isin(epi_ids)]

    # Join subsets together & convert missing values to None
    final_df = (all_eps.merge(ratings, on=['tconst'])
        .merge(basics, on=['tconst'])
        .replace('\\N', None)
    )
    final_df = final_df.astype({
            'seasonNumber': int,
            'episodeNumber': int,
            'runtimeMinutes': float,
        }
    )
    final_df = (final_df.sort_values(by=['seasonNumber', 'episodeNumber'])
        .reset_index(drop=True)
    )
    #TO DO: Correct for EPISODE NUMBERING MISMATCH.
    return final_df


# Notes
# EPISODE_LINK has 174 rows instead of 180 on wiki:
# # considers S5E18-19 as 1 big episode (Raincoats) stored as ep 18 but no ep 19
# # Omits S6E14-15 (The Highlights of 100) -- contains no new content. No ep 14 or 15
# # Omits S9E21-22 (The Clip Show) -- contains no new content. No ep 21 or 22
# # Coniders S9E23-24 (The Finale) as 1 big episode stores as ep 23 but no ep 24/

# IMDB has 173 rows:
# # Considers S3Ep17-18 (The Boyfriend) as 1 episode. Numbering after differs
# # DOES consider S5E18-19 as 1 big episode #18 (Raincoats).
# # # but also puts extra entry for #19 that can can remove!
# #  DOES NOT omit S6E14-15 (The Highlights of 100). Instead stores as Ep 14. Numbering after differs
# # Considers S7E14-15 as 1 big episode (The Cadillac) as ep 14. Numbering after differs
# # Considers S7E21-22 as 1 big episode (The Bottle Deposit) as ep 20. Numbering after differs
# # DOES NOT omits S9E21-22 (The Clip Show). Instead stores as Ep 21. Numbering after differs
# # DOES Coniders S9E23-24 (The Finale) as 1 big episode but stores as ep 22.
