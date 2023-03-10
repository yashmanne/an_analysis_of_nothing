"""
This script contains the contents of the Episode Recommender
page and is called by the main app.py script.

This script requires Streamlit and pandas be installed.
This script uses functions contained in the recommender.py
located in the utils folder.
"""

import streamlit as st
import pandas as pd

from utils import recommender

def main():
    """
    This function executes the Streamlit formatted HTML
    displayed on the Episode Recommender webpage and utilizes user
    inputs to calculate recommened episodes.

    Arguments: None
    Returns: None

    User Inputs
    ------------
        1. num_episodes : int
        2. title : List of strings
        3. streamlit button : boolean
    """
    st.markdown("""<h2 style='text-align: center; color: white;'><br>
                Episode Recommender<br><br></h2>""",
                unsafe_allow_html=True)

    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                Please answer the follow prompts for
                episode recommendations:<br><br></h6>""",
                unsafe_allow_html=True)

    num_ep = st.selectbox(
        "How many episodes do you want recommended to you?",
        options=[1,2,3,4,5],
        index=0
        )

    imdb_df_rec = pd.DataFrame(st.session_state.df_imdb)
    scripts_df_rec = pd.DataFrame(st.session_state.df_dialog)

    title = st.multiselect(
        label="Enter the title of episodes you've enjoyed.",
        options=imdb_df_rec["Title"].unique()
    )

    st.markdown("""<body><p><small><i>
                *If you don't know the title of your
                favorite episode, navigate to the Episode
                Query page to search for the title*
                </i></small></p></body>""",
                unsafe_allow_html=True)

    left_4, middle_4, right_4 = st.columns([1,5,1])
    with middle_4:
        st.image('./static/images/giphy.gif')
    with left_4 and right_4:
        pass

    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                Check box to enter and uncheck to reset:</h6>""",
                unsafe_allow_html=True)

    recs = st.session_state.recommender

    if st.button("Hiii"):
        ranked_ep = recs.find_closest_episodes(num_episodes=num_ep,
                                                title_list=title)
        st.dataframe(ranked_ep[["Title", "Season", "EpisodeNo"]],
                            use_container_width=True)
