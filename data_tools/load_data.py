"""
Contains functions to load data from online sources.
"""
# import os
# import numpy as np
import pandas as pd

from . import data_constants

def read_scripts():
    """
    Read in `Seinfeld Chronicles` script data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    df = pd.read_csv(data_constants.SCRIPTS_LINK)
    # pylint: disable=no-member
    df.drop(columns=df.columns[0], inplace=True)
    # pylint: disable=no-member
    df = df.astype({
            'Season': int,
            'EpisodeNo': int
        }
    )
    # Fix Season 1. Ep1 is combination of Ep1&2. Need to split into 2.
    # Episode 1 ends at Line 210.
    # Map Ep1 to 0, then add 1 to all episodes in season 1.
    df.loc[0:210, 'EpisodeNo'] = 0
    season_mask = df.Season==1
    df.loc[season_mask, 'EpisodeNo'] = df.loc[season_mask, 'EpisodeNo'] + 1
    df.loc[season_mask, 'SEID'] = df.loc[season_mask, 'SEID'].str[:4] +\
        df.loc[season_mask, 'EpisodeNo'].astype(str).str.pad(2,fillchar='0')
    return df

def read_episode_info():
    """
    Read in `Seinfeld Chronicles` episode data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    df = pd.read_csv(data_constants.EPISODE_LINK)
    # pylint: disable=no-member
    df.drop(columns=df.columns[0], inplace=True)
    # pylint: disable=no-member
    df = df.astype({
            'Season': int,
            'EpisodeNo': int
        }
    )
    # Fix Season 1's Mapping (have 2 Ep 1s)
    # Remap from 1,1,2,3,4 into 1,2,3,4,5
    season_mask = df.Season==1
    for ind in df.loc[season_mask].index:
        df.loc[ind, 'EpisodeNo'] = ind + 1
        df.loc[ind, 'SEID'] = f'S01E{ind + 1:02d}'
    return df

def read_imdb_metadata():
    """
    Read in `Seinfeld Chronicles` episode data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    seinfeld_id = data_constants.SEINFELD_PARENT_TCONST

    # Gather all episode metadata
    print('\t Gathering Episode Info...')
    all_eps = pd.read_csv(data_constants.IMDB_EPISODE, delimiter='\t')
    all_eps = all_eps[all_eps.parentTconst == seinfeld_id]
    #   Season 5, Episode 19 doubled in data.
    epi_ids = set(all_eps['tconst'].values) - {'tt19390512'}
    # Gather all rating data
    print('\t Gathering Rating Data...')
    ratings = pd.read_csv(data_constants.IMDB_RATING, delimiter='\t')
    ratings = ratings[ratings.tconst.isin(epi_ids)]
    # Gather additional metadata
    print('\t Gathering Title & Run Time Information...')
    basics = pd.read_csv(data_constants.IMDB_BASICS, delimiter='\t',
        usecols=['tconst', 'originalTitle', 'runtimeMinutes']
    )
    basics = basics[basics.tconst.isin(epi_ids)]
    # Gather all episode summary and keyword data
    print('\t Gathering Episode Descriptions, Summaries, and Keywords...')
    summaries = pd.read_csv(data_constants.IMDB_SUMMARIES)
    # Join subsets together & convert missing values to None
    final_df = (all_eps.merge(ratings, on=['tconst'])
        .merge(basics, on=['tconst'])
        .merge(summaries, on=['tconst'])
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
    # Correct episode number so it matches that of Kaggle/Wiki
    map_wiki = data_constants.MAP_IMDB_WIKI
    map_netflix = data_constants.MAP_IMDB_NETFLIX
    final_df['EpisodeNo'] = (final_df[['seasonNumber', 'episodeNumber']]
        .apply(lambda x: map_wiki[x[0]].get(x[1], x[1]), axis=1)
    )
    final_df['EpiNo_Netflix'] = (final_df[['seasonNumber', 'episodeNumber']]
        .apply(lambda x: map_netflix[x[0]].get(x[1], x[1]), axis=1)
    )
    # Remove other redundant columns & clean up order
    final_df.drop(columns=['episodeNumber', 'parentTconst'], inplace=True)
    final_df.rename(columns={'seasonNumber': 'Season'}, inplace=True)

    final_df = final_df[
        ['tconst', 'originalTitle', 'Season', 'EpisodeNo', 'EpiNo_Netflix',
         'runtimeMinutes', 'numVotes', 'averageRating',
         'Description', 'Summaries', 'keyWords']]
    final_df = final_df.astype({
            'EpiNo_Netflix': int,
            'runtimeMinutes': float,
        }
    )
    return final_df


def get_final_data(merge=False, load_cached=False):
    """
    Collect all data sets using the above helper functions.

    :param merge: boolean, whether or not to merge all data.
    :param load_cached: boolean, whether or not to load previously cached
                        data files
    :return: 2 Dataframes (1 Metadata, 1 scripts)
            or 1 if merge==True
    """
    # Try loading cached:
    if load_cached:
        try:
            meta = pd.read_csv(data_constants.PROCESSED_METADATA)
            scripts = pd.read_csv(data_constants.PROCESSED_SCRIPTS)
            return meta, scripts
        # pylint: disable=broad-except
        except Exception:
            print("Couldn't load cached files. Will start from scratch.")
    # The following episodes are the second part of a 2-part episode
    # that is merged for the IMDb data so they must be removed.
    kaggle_episodes_to_remove = ['S03E18', 'S04E24', 'S07E15', 'S07E22']
    # Get Kaggle Script Data
    print('Gathering Script Data...')
    scripts = read_scripts()
    # Get Kaggle Data Metadata
    print('Gathering Kaggle Metadata...')
    ep_info = read_episode_info()
    # Get IMDb Data:
    print('Gathering IMDb Data...')
    imdb_df = read_imdb_metadata()

    # Remove 2nd of 2-part episodes to match IMDb
    for epi in kaggle_episodes_to_remove:
        ep_number = int(epi[4:])
        prev_ep = epi[:4] + f'{ep_number-1:02d}'
        # pylint: disable=no-member
        scripts.loc[scripts.SEID==epi, 'SEID'] = prev_ep

    ep_info = ep_info[
        ~ep_info.SEID.isin(kaggle_episodes_to_remove)]

    # Merge Data Together
    merged_df = ep_info.merge(imdb_df,
        on=['Season', 'EpisodeNo'], how='left')
    merged_df.drop(columns=['Title'], inplace=True)
    merged_df.rename(columns={'originalTitle': 'Title'}, inplace=True)

    scripts.drop(columns=['EpisodeNo'], inplace=True)
    scripts['EpisodeNo'] = scripts.SEID.str[4:].astype(int)

    if merge:
        merged_df.drop(columns=['Season', 'EpisodeNo'], inplace=True)
        # pylint: disable=no-member
        all_merged = scripts.merge(merged_df, on = 'SEID', how='left')
        return all_merged

    return merged_df, scripts


if __name__ == '__main__':
    pass


# pylint: disable=pointless-string-statement
"""
NOTES:
# EPISODE_LINK has 174 rows instead of 180 on wiki:
# # considers S5E18-19 as 1 big episode (Raincoats) stored as ep 18 but no ep 19
# # Omits S6E14-15 (The Highlights of 100) -- contains no new content. No ep 14 or 15
# # Omits S9E21-22 (The Clip Show) -- contains no new content. No ep 21 or 22
# # Coniders S9E23-24 (The Finale) as 1 big episode stores as ep 23 but no ep 24/

# IMDB has 173 rows:
# # Considers S3Ep17-18 (The Boyfriend) as 1 episode. Numbering after differs
# # Considers S4Ep23-24 (The Pilot) as 1 episode. Numbering after differs
# # DOES consider S5E18-19 as 1 big episode #18 (Raincoats).
# # # but also puts extra entry for #19 that can can remove!
# #  DOES NOT omit S6E14-15 (The Highlights of 100). Instead stores as Ep 14. Numbering after differs
# # Considers S7E14-15 as 1 big episode (The Cadillac) as ep 14. Numbering after differs
# # Considers S7E21-22 as 1 big episode (The Bottle Deposit) as ep 20. Numbering after differs
# # DOES NOT omits S9E21-22 (The Clip Show). Instead stores as Ep 21. Numbering after differs
# # DOES consider S9E23-24 (The Finale) as 1 big episode but stores as ep 22.

# Netflix follows IMDb numbering (after deleting 5.19) but also combines S4E3-4 into 1 episode.
"""