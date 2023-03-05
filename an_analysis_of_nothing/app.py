import pandas as pd
import numpy as np

import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

from utils import data_manager
from utils import recommender

st.set_page_config(layout="centered")

page_bg = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-color: black
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0)
}
[data-testid="stSidebar"] {
    background-color: #3580BB;
}
[data-testid="stMarkdownContainer"] {
    color: white;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

st.image('./static/images/analysis_of_nothing.png')

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Episode Recommender", "Query Episodes", "About Us"],
        icons=["house", "tv", 'search', 'people'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "white"}
        }
    )

if selected == "Home":

    st.markdown("""<h5 style='text-align: center; color: white;'>
            Explore your favorite Seinfeld moments, characters, and quotes!
            <br>Use the Episode Recommender to find an episode that's
            sure to make you laugh.</h5>""",
            unsafe_allow_html=True)

    left_1, middle_1, right_1 = st.columns(3)
    with middle_1:
        st.image('./static/images/lead.png')

    try:
        # Load dataframes into session state once
        if ("df_imdb" not in st.session_state) or ("df_dialog" not in st.session_state):
            st.session_state.df_imdb, st.session_state.df_dialog = data_manager.load_data()
    except Exception as e:
        st.error("There was an issue loading data")

    dialog_df = pd.DataFrame(st.session_state.df_dialog)

    seasons = st.multiselect(
        'Select Season(s)',
        dialog_df["Season"].unique(),
        default=[1,2,3]
    )

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
                Lines Spoken by Character and Season</h5>""",
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

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
                Average Episode Rating</h5>""",
                unsafe_allow_html=True)
   
    imdb_df = pd.DataFrame(st.session_state.df_imdb)

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

if selected == "Episode Recommender":

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
    
    left_4, middle_4, right_4 = st.columns(3)
    with middle_4:
        st.image('./static/images/giphy.gif')
    
    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                Check box to enter and uncheck to reset:</h6>""",
                unsafe_allow_html=True)

    ready = st.checkbox(
        label="Ready!"
    )
    
    if ready:
        with st.spinner("Loading your episodes..."):
            recs = recommender.Recommender(imdb_df_rec,scripts_df_rec)
            ranked_ep = recs.find_closest_episodes(n=num_ep, title_list=title)
            st.dataframe(ranked_ep[["Title", "Season", "EpisodeNo"]], use_container_width=True)
if selected == "Query Episodes":
    st.title("hey girl")
if selected == "About Us":

    st.markdown("""<h2 style='text-align: center; color: white;'><br>
                About Us<br><br></h2>""",
                unsafe_allow_html=True)
    
    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                For DATA515 Software Design for Data Scientists
                course at the University of Washington, we created
                web application for Seinfeld fans to explore
                and query dialogue snippets, identify correlations between
                character appearances and audience ratings, and chronicle
                appearances of various characters across the series.</h6>""",
                unsafe_allow_html=True)
   
    st.markdown("""<h6 style='text-align: left; color: white;'><br>
                Creators:</h6>""",
                unsafe_allow_html=True)
   
    left_2, right_2 = st.columns(2)
    with left_2:
        st.image('./static/images/kramer_.jpg', width=314)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Yash Manne<br>
                Project Manager</h6>""",
                unsafe_allow_html=True)
    with right_2:
        st.image('./static/images/elaine_.jpg', width=345)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Aditi Shrivastava<br>
                Developer<br><br></h6>""",
                unsafe_allow_html=True)
       
    left_3, right_3 = st.columns(2)
    with left_3:
        st.image('./static/images/newman_.jpg', width=314)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Yamina Katariya<br>
                UX Designer<br><br></h6>""",
                unsafe_allow_html=True)
    with right_3:
        st.image('./static/images/george_.jpg', width=345)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Chandler Audlt<br>
                Quality Assurance<br><br></h6>""",
                unsafe_allow_html=True)
