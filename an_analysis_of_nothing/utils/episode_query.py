"""
The following code contains utility functions for processing TV show dialogue data and 
searching for specific episodes based on keywords.
"""
import ast
import re
import string
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Search and selection tools: query_episodes, get_selected_row, map_imdb_to_scripts
def query_episodes(df_imdb, search_string):
    """
    Searches a pandas DataFrame for the closest matches to a given search string.

    Args:
        df_imdb (pandas.DataFrame): The DataFrame to search.
        search_string (str): The string to search for.

    Returns:
        pandas.DataFrame: The 5 closest matches to the search string.
    """
    try:
        # Preprocess the text data in the DataFrame
        df_imdb.loc[:, 'text'] = df_imdb.loc[:,
                                             'Summaries'].apply(preprocess_text)

        # Preprocess the search string
        query = preprocess_text(search_string)

        # Vectorize the text data in the DataFrame
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(df_imdb['text'])

        # Vectorize the search string
        query_vector = vectorizer.transform([query])

        # Calculate the cosine similarities between the search string and the text data
        cosine_similarities = cosine_similarity(
            query_vector, vectors).flatten()

        # Get the top 5 closest matches
        top_matches = cosine_similarities.argsort()[:-6:-1]

        return df_imdb.iloc[top_matches]
    
    except Exception as e:
        # If an error occurs, log the error message and return the original DataFrame
        st.error(str(e))
        return df_imdb
    
    
def get_selected_row(search_results):
    """
    Get a subset of the input dataframe containing only the selected episode, 
    as inputted by the user. 

    Args:
        search_results: a Pandas DataFrame as outputted by query_episodes.

    Returns:
        response (pd.DataFrame): a DataFrame containing all 
        metadata for the row selected by the user.
    """
    try:
        search_results = search_results[['Title', 'EpisodeNo']]

        # Create a grid builder object to process user selections
        gb = GridOptionsBuilder.from_dataframe(search_results)
        gb.configure_default_column(enablePivot = True, 
                                    enableValue = True, 
                                    enableRowGroup = True)
        gb.configure_column('EpisodeNo', min_column_width=1)
        gb.configure_selection(use_checkbox = True)
        gb.configure_auto_height(False)
        gridoptions = gb.build()
        
        # Load the grid options into an AgGrid object
        response = AgGrid(search_results, 
                          gridOptions = gridoptions,  
                          enable_enterprise_modules = True, 
                          update_mode = GridUpdateMode.MODEL_CHANGED, 
                          data_return_mode = DataReturnMode.FILTERED_AND_SORTED)

        # Convert the AgGrid into a pandas dataframe row
        return pd.DataFrame(response['selected_rows'])
    
    except Exception as e:
        # If an error occurs, log the error message and return the original DataFrame
        st.error(str(e))
        return response
    
def map_imdb_to_scripts(df_imdb, df_script):
    """
    Create an SEID column in the IMDb dataframe that corresponds
    to the scripts dataframe SEID column.
    
    Args:
        df_imdb (pandas.DataFrame): The DataFrame of IMDb data.
        df_script (pandas.DataFrame): The DataFrame of script data.
    
    Returns:
    
    """
    # Add columns for the season and episode numbers and the SEID
    df_imdb['SID'] = df_imdb['Season'].apply(lambda x: '{:02d}'.format(x))
    df_imdb['EID'] = df_imdb['EpisodeNo'].apply(
        lambda x: '{:02d}'.format(x))
    df_imdb['SEID'] = 'S' + df_imdb['SID'] + 'E' + df_imdb['EID']
    
    return df_imdb
    
    
# Sidebar filter tools: get_characters, get_ratings, get_seasons, draw_sidebar
def get_characters(df_imdb, df_script, char_choice):
    """
    Extract episodes from the IMDb containing the user inputted
    characters in char_choice.
    
    Args:
        df_imdb (pandas.DataFrame): The DataFrame of IMDb data.
        df_script (pandas.DataFrame): The DataFrame of script data.
        char_choice (list): A list of characters to search for.
    
    Returns:
        pandas.DataFrame: an IMDb DataFrame of only the episodes that 
        contain dialogue by the selected character(s).
    
    """
#     char_list = df_script.groupby('SEID')['Character'].apply(list)
    
#     df_imdb = df_imdb.sort_values('SEID')
#     df_char = pd.DataFrame(char_list).reset_index()
#     df_char = df_char[df_char.SEID.isin(df_imdb.SEID)].sort_values('SEID')
#     df_imdb['char_list'] = df_char['Character']
#     df_imdb = df_imdb.dropna()

#     df_imdb['char_check'] = df_imdb.char_list.apply(lambda x: all(char in x for char in char_choice))
#     return df_imdb[df_imdb.char_check == True]
    return df_imdb
    
    
def get_seasons(df_imdb, season_choice):
    """
    Extract episodes from the IMDb containing the user inputted
    seasons in char_choice.
    
    Args:
        df_imdb (pandas.DataFrame): The DataFrame of IMDb data.
        season_choice (list): A list of seasons to search for.
    
    Returns:
        pandas.DataFrame: an IMDb DataFrame of only the episodes that 
        are from the selected season(s).
    
    """
    return df_imdb[df_imdb.Season.isin(season_choice)]
    
    
def get_ratings(df_imdb, rating_choice):
    """
    Extract episodes from the IMDb containing the user inputted
    ratings in rating_choice.
    
    Args:
        df_imdb (pandas.DataFrame): The DataFrame of IMDb data.
        rating_choice (tuple): A tuple range of ratings to search for.
    
    Returns:
        pandas.DataFrame: an IMDb DataFrame of only the episodes that 
        are rated within the selected rating range.
    
    """
    upper = df_imdb[df_imdb.averageRating <= rating_choice[1]]
    return upper[upper.averageRating >= rating_choice[0]]


# Sentiment Analysis tools: get_script_from_ep, extract_argmax, extract_emotions, preprocess_text
def get_script_from_ep(df_imdb, df_script, episode):
    """
    Returns a DataFrame of dialogue occurrences for a given episode.

    Args:
    df_imdb (pandas.DataFrame): The DataFrame of IMDb data.
    df_script (pandas.DataFrame): The DataFrame of script data.
    episode: The title of the episode selected by the user.

    Returns:
    pandas.DataFrame: The DataFrame of dialogue occurrences.
    """
    try:
        # Add columns for the season and episode numbers and the SEID
        df_imdb = map_imdb_to_scripts(df_imdb, df_script)

        # Filter the IMDb data for the selected episode
        selected_episodes = df_imdb.loc[df_imdb['Title'] == episode]

        # Filter the script data for the selected SEIDs
        selected_dialogue = df_script.loc[df_script['SEID'].isin(
            selected_episodes['SEID'].unique())]

        return selected_dialogue
    
    except Exception as e:
        # If an error occurs, log the error message and return the original DataFrame
        st.error(str(e))
        return df_script
    
    
def extract_argmax(row):
    """
    Extract the maximum emotion from a row of emotions as a string.

    Args:
        row: a Pandas Series containing emotion data in the form of a dictionary.

    Returns:
        The key corresponding to the maximum value in the dictionary, 
        or 'No Emotion' if all values are zero.
    """
    try:
        emotions_dict = ast.literal_eval(row['sentiment'])
        if all(value == 0 for value in emotions_dict.values()):
            return 'No Emotion'
        else:
            return max(emotions_dict, key=emotions_dict.get)
        
    except Exception as e:
        # If an error occurs, log the error message and return the original DataFrame
        st.error(str(e))
        return pd.Series


def extract_emotions(row):
    """
    Extract individual emotions from a row of emotions as separate columns.

    Args:
        row: a Pandas Series containing emotion data in the form of a dictionary.

    Returns:
        A Pandas Series containing the individual emotion values for the row.
    """
    try:
        emotions_dict = ast.literal_eval(row['sentiment'])
        happy = emotions_dict.get('Happy', 0.0)
        angry = emotions_dict.get('Angry', 0.0)
        surprise = emotions_dict.get('Surprise', 0.0)
        sad = emotions_dict.get('Sad', 0.0)
        fear = emotions_dict.get('Fear', 0.0)
        return pd.Series({'Happy': happy, 
                          'Angry': angry, 
                          'Surprise': surprise, 
                          'Sad': sad, 
                          'Fear': fear})
    
    except Exception as e:
        # If an error occurs, log the error message and return the original DataFrame
        st.error(str(e))
        return pd.Series({'Happy': 0, 'Angry': 0, 'Surprise': 0, 'Sad': 0, 'Fear': 0})


def preprocess_text(text):
    """
    Preprocess text by removing numbers, punctuation, and stop words, and converting to lowercase.

    Args:
        text: a string of text to be preprocessed.

    Returns:
        The preprocessed text.
    """
    try:
        if not isinstance(text, str):
            raise TypeError('Text argument must be a string')

        stop_words = ['a', 'an', 'the', 'in', 'on',
                      'at', 'to', 'of', 'for', 'and', 'or']
        text = re.sub(r'\d+', '', text)  # remove numbers
        text = text.translate(str.maketrans(
            '', '', string.punctuation))  # remove punctuation
        text = text.lower()  # convert to lowercase
        # remove stop words
        text = ' '.join([word for word in text.split()
                        if word not in stop_words])
        return text
    
    except Exception as e:
        # If an error occurs, log the error message and return the original DataFrame
        st.error(str(e))
        return ''
