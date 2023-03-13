"""
This script contains the contents of the Episode Recommender
page and is called by the main app.py script.

This script requires Streamlit and pandas be installed.
This script uses functions contained in the recommender.py
located in the utils folder.
"""

import streamlit as st
import pandas as pd
from utils import episode_query


def main():
    """
    This function executes the Streamlit formatted HTML
    displayed on the Episode Recommender webpage and utilizes user
    inputs to calculate recommended episodes.

    Arguments: None
    Returns: None

    User Inputs
    ------------
        1. num_episodes : int
        2. title : List of strings
        3. streamlit button : boolean
    """
    st.markdown("""<h2 style='text-align: center; color: #031B28;'>
                Episode Recommender<br></h2>""",
                unsafe_allow_html=True)

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
                Please answer the follow prompts to recieve
                episode recommendations.<br><br></h5>""",
                unsafe_allow_html=True)

    st.markdown("""<h6 style='text-align: center; color: white;'><br>
                How many episodes do you want recommended to you?</h6>""",
                unsafe_allow_html=True)

    num_ep = st.selectbox(
        "How many episodes do you want recommended to you?",
        label_visibility="collapsed",
        options=[1,2,3,4,5],
        index=0
        )

    imdb_df_rec = pd.DataFrame(st.session_state.df_imdb)

    st.markdown("""<h6 style='text-align: center; color: white;'><br>
                Enter the title of episodes you've enjoyed.</h6>""",
                unsafe_allow_html=True)

    title = st.multiselect(
        label="Enter the title of episodes you've enjoyed.",
        label_visibility="collapsed",
        options=imdb_df_rec["Title"].unique()
    )

    st.markdown("""<p style='font-style: italic; text-align:center;'>
                If you don't know the title of the episode, navigate to the Episode
                Query page to search for the title.
                </p>""",
                unsafe_allow_html=True)

    left_4, middle_4, right_4 = st.columns([1,5,1])
    with middle_4:
        st.image('./static/images/giphy.gif')
    with left_4 and right_4:
        pass

    recs = st.session_state.recommender

    if title:

        st.markdown("""
            <h6 style='text-align: center; color: white; text-style: italic;'>
            Select an episode to learn more.</h6>""",
            unsafe_allow_html=True)

        col2_1, col2_2, col2_3 = st.columns([.25, 3.5, .25])
        ranked_ep = recs.find_closest_episodes(num_episodes=num_ep,
                                                title_list=title)
        with col2_2:
            response = episode_query.get_selected_row(ranked_ep)
        with col2_1 and col2_3:
            pass

        if len(response) == 0:
            desc = 'Choose an episode to view its IMDb description!'
        else:
            selected_imdb = imdb_df_rec[
                imdb_df_rec.Title == response['Title'].values[0]]

        # Metadata
        if len(response) == 0:
            desc = 'Choose an episode to view its IMDb description!'
        else:
            selected_imdb = imdb_df_rec[
                imdb_df_rec.Title == response['Title'].values[0]]
            desc = selected_imdb['Description'].values[0]
        # Metadata
        st.markdown("""<h3 style='text-align: left; color: #031B28;'>
                IMDb Episode Description:</h3>""",
                unsafe_allow_html=True)
        st.markdown(desc)
    elif not title:
        st.markdown("""<h6 style='text-align: center; color: white;
                font-style: italic;'><p>
                Please select at least one episode title to recieve
                recommendations.</p></h6>""",
                unsafe_allow_html=True)
