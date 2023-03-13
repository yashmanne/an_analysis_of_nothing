"""
This script creates and runs the streamlit website,
and calls each subpage to be run when selected.

This script requires Streamlit to be installed.
"""
import os

import streamlit as st
from streamlit_option_menu import option_menu

from app_pages import write_home_page
from app_pages import write_recommender_page
from app_pages import write_about_page
from app_pages import write_episode_query

cwd = os.getcwd()
base_path = cwd.split("an_analysis_of_nothing", maxsplit=1)[0]
curr_path = base_path + \
    'an_analysis_of_nothing/an_analysis_of_nothing/'

os.chdir(curr_path)

st.set_page_config(layout="centered")

st.markdown("""<style>
            [data-testid="stAppViewContainer"] > .main {
                background-image: url("https://www.pixelstalk.net/wp-content/uploads/images1/Free-download-central-park-backgrounds.jpg");
                background-position: center;
            }
            [data-testid="stSidebar"] {
                background-color: #889FB8;
            }
            [data-testid="stMarkdownContainer"] {
                color: white;
            }
            [data-testid="stVerticalBlock"] {
                background-color: #889FB8;
            }
            [data-testid="stVerticalBlock"] {
                color: white;
            }
            </style>""", unsafe_allow_html=True)

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
    write_home_page.main()

if selected == "Episode Recommender":
    write_recommender_page.main()

if selected == "Query Episodes":
    write_episode_query.main()

if selected == "About Us":
    write_about_page.main()
