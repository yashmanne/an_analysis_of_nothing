"""
The following code contains utility functions for processing TV show dialogue data and 
searching for specific episodes based on keywords.
"""
import ast
import re
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


def extract_argmax(row: pd.Series) -> str:
    """
    Extract the maximum emotion from a row of emotions as a string.

    Args:
        row: a Pandas Series containing emotion data in the form of a dictionary.

    Returns:
        The key corresponding to the maximum value in the dictionary, or 'No Emotion' if all values are zero.
    """
    try:
        emotions_dict = ast.literal_eval(row['sentiment'])
        if all(value == 0 for value in emotions_dict.values()):
            return 'No Emotion'
        else:
            return max(emotions_dict, key=emotions_dict.get)
    except Exception as e:
        st.error(str(e))
        return pd.Series


def getSelectedEp(df_imdb: pd.DataFrame, selected: pd.DataFrame) -> pd.DataFrame:
    """
    Get a subset of the input dataframe containing only the selected episodes.

    Args:
        df_imdb: a Pandas DataFrame containing TV show episode data.
        selected: a Pandas DataFrame containing episode IDs of the selected episodes.

    Returns:
        A Pandas DataFrame containing only the episodes with IDs in the 'selected' DataFrame.
    """
    try:
        return df_imdb[df_imdb['SEID'].isin(selected['SEID'].unique())]
    except Exception as e:
        st.error(str(e))
        return df_imdb


def extract_emotions(row: pd.Series) -> pd.Series:
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
        return pd.Series({'Happy': happy, 'Angry': angry, 'Surprise': surprise, 'Sad': sad, 'Fear': fear})
    except Exception as e:
        st.error(str(e))
        return pd.Series({'Happy': 0, 'Angry': 0, 'Surprise': 0, 'Sad': 0, 'Fear': 0})


def preprocess_text(text: str) -> str:
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
        st.error(str(e))
        return ''


def search_dataframe(df_imdb, search_string):
    """
    Searches a pandas DataFrame for the closest matches to a given search string.

    Args:
    df_imdb (pandas.DataFrame): The DataFrame to search.
    search_string (str): The string to search for.

    Returns:
    pandas.DataFrame: The closest matches to the search string.
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


def get_occurrences(df_imdb, df_scripts, ids):
    """
    Returns a DataFrame of dialogue occurrences for a given set of episode IDs.

    Args:
    df_imdb (pandas.DataFrame): The DataFrame of IMDb data.
    df_scripts (pandas.DataFrame): The DataFrame of script data.
    ids (list): The list of episode IDs to search for.

    Returns:
    pandas.DataFrame: The DataFrame of dialogue occurrences.
    """
    try:
        # Add columns for the season and episode numbers and the SEID
        df_imdb['SID'] = df_imdb['Season'].apply(lambda x: '{:02d}'.format(x))
        df_imdb['EID'] = df_imdb['EpisodeNo'].apply(
            lambda x: '{:02d}'.format(x))
        df_imdb['SEID'] = 'S' + df_imdb['SID'] + 'E' + df_imdb['EID']

        # Filter the IMDb data for the selected episode IDs
        selected_episodes = df_imdb.loc[df_imdb['Title'].isin(ids)]

        # Filter the script data for the selected SEIDs
        selected_dialogue = df_scripts.loc[df_scripts['SEID'].isin(
            selected_episodes['SEID'].unique())]

        return selected_dialogue
    except Exception as e:
        st.error(str(e))
        return df_scripts
        # If an error occurs, log the error message and return the original DataFrame
