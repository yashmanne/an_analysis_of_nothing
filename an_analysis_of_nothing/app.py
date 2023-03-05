"""
This script creates and runs the streamlit website,
and calls each subpage to be run when selected.

This script requires Streamlit to be installed.
"""

import streamlit as st
from streamlit_option_menu import option_menu

from app_pages import write_home_page
from app_pages import write_recommender_page
from app_pages import write_about_page

st.set_page_config(layout="centered")

st.markdown("""<style>
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
    st.title("hey girl")

if selected == "About Us":
    write_about_page.main()
