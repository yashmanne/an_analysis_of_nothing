"""
This script contains the contents of the Home page
and is called by the main app.py script.

This script requires Streamlit, pandas, numpy, and
plotly.express be installed. This script uses functions
contained in the data_manager.py located in the utils folder.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import data_manager, recommender, episode_query


def main():
    """
    This function executes the Streamlit formatted HTML
    displayed on the Home webpage and displays interactive visualizations.

    Arguments: None
    Returns: None

    User Inputs
    ------------
        1. seasons : int
    """
    st.markdown("""<h2 style='text-align: center; color: #031B28;'>
            Home</h2>""",
            unsafe_allow_html=True)

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
            Explore your favorite Seinfeld moments, characters, and quotes!
            <br>Use the Episode Recommender to find an episode that's
            sure to make you laugh.</h5>""",
            unsafe_allow_html=True)

    left_1, middle_1, right_1 = st.columns([1,5,1])
    with middle_1:
        st.image('./static/images/lead.png')
    with left_1 and right_1:
        pass

    try:
        # Load dataframes into session state once
        if ("df_imdb" not in st.session_state) or ("df_dialog" not in st.session_state):
            st.session_state.df_imdb, st.session_state.df_dialog = data_manager.load_data()
    except FileNotFoundError:
        st.error("There was an issue loading data")

    dialog_df = pd.DataFrame(st.session_state.df_dialog)
    imdb_df = pd.DataFrame(st.session_state.df_imdb)

    try:
        # Load recommender into session state once
        if "recommender" not in st.session_state:
            st.session_state.recommender = recommender.Recommender(
                imdb_df, dialog_df)
        if 'query' not in st.session_state:
            st.session_state.query = episode_query.load_corpus(imdb_df, dialog_df)
    except ValueError:
        st.error("Failed to instantiate class")

    st.markdown("""<h6 style='text-align: center; color: white;'><br>
                Select Season(s)</h6>""",
                unsafe_allow_html=True)

    seasons = st.multiselect(
        'Select Season(s)',
        label_visibility="collapsed",
        options=dialog_df["Season"].unique(),
        default=[1,2,3]
    )

    st.markdown("""<h4 style='text-align: center; color: #031B28;'><br>
                Lines Spoken by Character and Season</h4>""",
                unsafe_allow_html=True)

    selected_seasons = np.in1d(dialog_df["Season"], seasons)
    season_df = dialog_df[selected_seasons]

    main_four = ["JERRY", "GEORGE", "ELAINE", "KRAMER"]
    characters = np.in1d(season_df["Character"], main_four )
    character_df = season_df[characters]

    histogram = px.histogram(
        data_frame = character_df,
        x = "Character",
        template="presentation",
        color = "Season"
    )
    histogram.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        legend_font_color="white",
        legend_title_font_color="white",
        newshape_line_color = "white"
    )
    histogram.update_xaxes(
        title_font_color="white",
        tickfont_color="white"
    )
    histogram.update_yaxes(
        title_font_color="white",
        tickfont_color="white"
    )

    st.plotly_chart(histogram)

    one, two, three, four = st.columns(4)
    with one:
        st.image('./static/images/jerry.png', width=190)
    with two:
        st.image('./static/images/george.png', width=170)
    with three:
        st.image('./static/images/kramer.png', width=195)
    with four:
        st.image('./static/images/elaine.png', width=210)

    st.markdown("""<h4 style='text-align: center; color: #031B28;'><br>
                Average Episode Rating</h4>""",
                unsafe_allow_html=True)

    chosen_seasons = np.in1d(imdb_df["Season"], seasons)
    imdb_season_df = imdb_df[chosen_seasons]

    line_chart = px.line(
        data_frame = imdb_season_df,
        x = "SEID",
        y = "averageRating",
        labels = {
            "averageRating": "Average Rating",
            "SEID": "Season and Episode"
        },
        template = "presentation",
        color = "Season"
    )
    line_chart.update_traces(
        mode = "markers+lines",
        hovertemplate=None
    )
    line_chart.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        legend_font_color="white",
        legend_title_font_color="white",
        newshape_line_color = "white"
    )
    line_chart.update_xaxes(
        title_font_color="white",
        tickfont_color="white"
    )
    line_chart.update_yaxes(
        title_font_color="white",
        tickfont_color="white"
    )

    st.plotly_chart(line_chart)
