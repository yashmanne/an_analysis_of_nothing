"""
This script contains the contents of the Episode Recommender
page and is called by the main app.py script.

This script requires Streamlit and pandas be installed.
This script uses functions contained in the recommender.py
located in the utils folder.
"""

import streamlit as st
import pandas as pd

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
    st.markdown("""<h2 style='text-align: center; color: white;'>
                Episode Recommender<br></h2>""",
                unsafe_allow_html=True)

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
                Please answer the follow prompts to recieve
                episode recommendations.<br><br></h5>""",
                unsafe_allow_html=True)

    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                How many episodes do you want recommended to you?</h6>""",
                unsafe_allow_html=True)

    num_ep = st.selectbox(
        "How many episodes do you want recommended to you?",
        label_visibility="collapsed",
        options=[1,2,3,4,5],
        index=0
        )

    imdb_df_rec = pd.DataFrame(st.session_state.df_imdb)

    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                Enter the title of episodes you've enjoyed.</h6>""",
                unsafe_allow_html=True)

    title = st.multiselect(
        label="Enter the title of episodes you've enjoyed.",
        label_visibility="collapsed",
        options=imdb_df_rec["Title"].unique()
    )

    st.markdown("""<p style='font-style: italic; text-align:center;'>
                *If you don't know the title the episode, navigate to the Episode
                Query page to search for the title*
                </p>""",
                unsafe_allow_html=True)

    left_4, middle_4, right_4 = st.columns([1,5,1])
    with middle_4:
        st.image('./static/images/giphy.gif')
    with left_4 and right_4:
        pass

    recs = st.session_state.recommender
    left_5, middle_5, right_5 = st.columns([3,1,3])
    with middle_5:
        butt = st.button("Submit")
    with left_5 and right_5:
        pass

    if butt and title:
        ranked_ep = recs.find_closest_episodes(num_episodes=num_ep,
                                                title_list=title)
        st.dataframe(ranked_ep[["Title", "Season", "EpisodeNo"]],
                            use_container_width=True)
    elif butt and not title:
        st.markdown("""<h6 style='text-align: center; color: white;
                font-style: italic;'><p>
                Please select at least one episode title to recieve
                recommendations.</p></h6>""",
                unsafe_allow_html=True)
