"""
The following code contains utility functions for processing
TV show dialogue data and searching for specific episodes
based on keywords.
"""

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, \
    GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
from sentence_transformers import SentenceTransformer, util
import torch

from . import data_manager


def filter_search_results(search_string, season_choice, rating_choice,
                          char_choice, df_imdb, df_script):
    """
    Filters imdb dataframe based on query from user and sidebar options.
    Args:
        search_string (str): The user inputted string to search for.
        season_choice (list): The user inputted list of seasons to filter,
            or None if not specified.
        rating_choice (tuple): The user inputted range of ratings to filter,
            or None if not specified.
        char_choice (list): The user inputted list of characters to filter,
            or None if not specified.
        df_imdb (pd.DataFrame): The IMDb metadata DataFrame
            (st.session_state.df_imdb).
        df_script (pd.DataFrame): The scripts DataFrame
            (st.session_state.df_dialog).
    Returns:
        tuple: The filtered df_imdb dataframe, and the closest matches to the
            search string from the filtered dataframe.
    """
    if season_choice and rating_choice and char_choice:
        filtered_df = get_characters(df_imdb,
                                     df_script,
                                     char_choice)
        filtered_df = get_ratings(filtered_df,
                                  rating_choice)
        filtered_df = get_seasons(filtered_df,
                                  season_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    if season_choice and rating_choice is None and char_choice is None:
        filtered_df = get_seasons(df_imdb,
                                  season_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    if season_choice is None and rating_choice and char_choice is None:
        filtered_df = get_ratings(df_imdb,
                                  rating_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    if season_choice is None and rating_choice is None and char_choice:
        filtered_df = get_characters(df_imdb,
                                     df_script,
                                     char_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    if season_choice is None and rating_choice and char_choice:
        filtered_df = get_characters(df_imdb,
                                     df_script,
                                     char_choice)
        filtered_df = get_ratings(filtered_df,
                                  rating_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    if season_choice and rating_choice is None and char_choice:
        filtered_df = get_seasons(df_imdb,
                                  season_choice)
        filtered_df = get_characters(filtered_df,
                                     df_script,
                                     char_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    if season_choice and rating_choice and char_choice is None:
        filtered_df = get_ratings(df_imdb,
                                  rating_choice)
        filtered_df = get_seasons(filtered_df,
                                  season_choice)
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results
    else:
        filtered_df = df_imdb
        search_results = query_episodes(filtered_df,
                                        df_script,
                                        search_string)
        return filtered_df, search_results


def load_corpus(df_imdb, df_script):
    """
    Load sentence transformer and embedder for episode querying.
    Args:
        df_imdb (pd.DataFrame): The IMDb metadata DataFrame
            (st.session_state.df_imdb).
            Unused but passed to maintain backwards compatibility.
        df_script (pd.DataFrame): The scripts DataFrame
            (st.session_state.df_dialog).
    Returns:
        list: Dialogue and summaries for each episode in df_imdb.
        tensor: Vectorized corpus (embeddings).
        SentenceTransformer: BertModel for finding closest matches.
    """
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    # try: 'distilbert-base-nli-stsb-mean-tokens'
    corpus = df_script.Dialogue.values
    # corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    corpus_embeddings = data_manager.get_episode_query_tensors(num_shards=10)
    return corpus, corpus_embeddings, embedder


def query_episodes(df_imdb, df_script, query):
    """
    Searches a pandas DataFrame for the closest matches to the search string.
    Args:
        df_imdb (pd.DataFrame): The episode metadata DataFrame to search.
        df_script (pd.DataFrmame): The dialogues of each episode.
        query (str): The string to search for.
    Returns:
        pd.DataFrame: The 5 closest matches to the search string.
    """
    corpus, corpus_embeddings, embedder = st.session_state.query
    df = pd.DataFrame({'Dialogue': [], 'Index': [], 'Score' : []})
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    # Cosine-similarity and torch.topk for highest scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=500)
    for score, idx in zip(top_results[0], top_results[1]):
        df = pd.concat([df, pd.Series({'Dialogue': corpus[idx],
                                       'Index': int(idx),
                                       'Score': score}).to_frame().T],
                       ignore_index=True)
    # Map to df_imdb
    df['SEID'] = df.Index.apply(lambda x: df_script.iloc[x].SEID)
    df = df[df.SEID.isin(df_imdb.SEID)]
    df['Title'] = df.Index.apply(lambda x: df_imdb[df_imdb.SEID == df_script.iloc[x]['SEID']]['Title'].values[0])
    df_imdb = df_imdb.loc[df_imdb.Title.isin(
        df.drop_duplicates(
        subset=['Title']).iloc[0:5].Title
    )]
    return df_imdb


def get_selected_row(search_results):
    """
    Get a subset of the input dataframe containing only the selected episode,
    as inputted by the user.
    Args:
        search_results (pd.DataFrame): a Pandas DataFrame as
            outputted by query_episodes.
    Returns:
        response (pd.DataFrame): a DataFrame containing all
            metadata for the row selected by the user.
    """
    search_results = search_results[
        ['SEID', 'Title', 'averageRating', 'Director', 'Writers']
    ]
    # Create a grid builder object to process user selections
    grid = GridOptionsBuilder.from_dataframe(search_results)
    grid.configure_default_column(
        enablePivot=True,
        enableValue=True,
        enableRowGroup=True)
    grid.configure_selection(use_checkbox=True)
    grid.configure_column('SEID', header_name="Episode ID",
                          min_column_width=1)
    grid.configure_column('averageRating', header_name="Rating",
                          min_column_width=1)
    grid.configure_auto_height(False)
    gridoptions = grid.build()
    # Load the grid options into an AgGrid object
    min_height = 70
    max_height = 800
    row_height = 30

    response = AgGrid(
        search_results,
        gridOptions=gridoptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        theme="streamlit",
        height=min(min_height + len(search_results) * row_height, max_height)
    )

    # Convert the AgGrid into a pandas dataframe row
    return pd.DataFrame(response['selected_rows'])


def get_characters(df_imdb, df_script, char_choice):
    """
    Extract episodes from the IMDb containing the user inputted
    characters in char_choice.
    Args:
        df_imdb (pd.DataFrame): The DataFrame of IMDb data.
        df_script (pd.DataFrame): The DataFrame of script data.
        char_choice (list): A list of characters to search for.
    Returns:
        pd.DataFrame: an IMDb DataFrame of only the episodes that
            contain dialogue by the selected character(s).
    """
    char_list = df_script.groupby('SEID')['Character'].apply(list)
    df_imdb = df_imdb.sort_values('SEID')
    df_char = pd.DataFrame(char_list).reset_index()
    df_char = df_char[df_char.SEID.isin(df_imdb.SEID)].sort_values('SEID')
    df_imdb['char_list'] = df_char['Character']
    df_imdb = df_imdb.dropna()
    df_imdb['char_check'] = df_imdb.char_list.apply(
        lambda x: all(char in x for char in char_choice))
    return df_imdb.loc[df_imdb.char_check == True]


def get_seasons(df_imdb, season_choice):
    """
    Extract episodes from the IMDb containing the user inputted
    seasons in char_choice.
    Args:
        df_imdb (pd.DataFrame): The DataFrame of IMDb data.
        season_choice (list): A list of seasons to search for.
    Returns:
        pd.DataFrame: an IMDb DataFrame of only the episodes that
            are from the selected season(s).
    """
    return df_imdb.loc[df_imdb.Season.isin(season_choice)]


def get_ratings(df_imdb, rating_choice):
    """
    Extract episodes from the IMDb containing the user inputted
    ratings in rating_choice.
    Args:
        df_imdb (pd.DataFrame): The DataFrame of IMDb data.
        rating_choice (tuple): A tuple range of ratings to search for.
    Returns:
        pd.DataFrame: an IMDb DataFrame of only the episodes that
            are rated within the selected rating range.
    """
    upper = df_imdb.loc[df_imdb.averageRating <= rating_choice[1]]
    return upper.loc[upper.averageRating >= rating_choice[0]]


def get_script_from_ep(df_imdb, df_script, episode):
    """
    Returns a DataFrame of dialogue occurrences for a given episode.
    Args:
        df_imdb (pd.DataFrame): The DataFrame of IMDb data.
        df_script (pd.DataFrame): The DataFrame of script data.
        episode: The title of the episode selected by the user.
    Returns:
        pd.DataFrame: The DataFrame of dialogue occurrences.
    """
    try:
        # Filter the IMDb data for the selected episode
        selected_episodes = df_imdb.loc[df_imdb['Title'] == episode]
        # Filter the script data for the selected SEIDs
        selected_dialogue = df_script.loc[df_script['SEID'].isin(
            selected_episodes['SEID'].unique())]
        return selected_dialogue
    except Exception as e:
        # If an error occurs,
        # log the error message and return the original DataFrame
        st.error(str(e))
        return df_script


def extract_emotions(row):
    """
    Extract individual emotions from a row of emotions as separate columns.
    Args:
        row: a Pandas Series containing emotion data.
    Returns:
        pd.Series: A series containing individual emotion values for the row.
    """
    happy = row['Happy']
    angry = row['Angry']
    surprise = row['Surprise']
    sad = row['Sad']
    fear = row['Fear']
    return pd.Series({'Happy': happy,
                      'Angry': angry,
                      'Surprise': surprise,
                      'Sad': sad,
                      'Fear': fear})


def extract_argmax(row):
    """
    Extract the maximum emotion from a row of emotions as a string.
    Args:
        row: a Pandas Series containing emotion data.
    Returns:
        str: The key corresponding to the maximum value in the dictionary,
        or 'No Emotion' if all values are zero.
    """
    emotions_dict = dict(extract_emotions(row))
    if all(value == 0 for value in emotions_dict.values()):
        return 'No Emotion'
    return max(emotions_dict, key=emotions_dict.get)
