"""
This script contains the contents of the Episode Querying
page and is called by the main app.py script.
This script uses functions contained in the episode_query.py
located in the utils folder.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from utils import episode_query


def main():
    """
    This function executes the Streamlit formatted HTML
    displayed on the Episode Querying webpage and utilizes user
    inputs to search for and display user input.
    Arguments: None
    Returns: None
    """
    # Intro text/logo
    # Load data
    df_imdb = pd.DataFrame(st.session_state.df_imdb)
    df_script = pd.DataFrame(st.session_state.df_dialog)

    # Titles, image, search bar
    st.markdown("""<h2 style='text-align: center; color: #031B28;'>
                        Episode Querying</h2>""",
                        unsafe_allow_html=True)

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
            Search for specific episodes from the show by entering
            keywords, concepts, or topics in the search bar below.
            Then, view sentiment statistics for the five queried episodes.
            <br><br></h5>""",
            unsafe_allow_html=True)

    left_5, middle_5, right_5 = st.columns([1.65,5,1])
    with middle_5:
        st.image('./static/images/elaine_typing.gif')
    with left_5 and right_5:
        pass

    # Configure sidebar
    st.sidebar.markdown("""<h2 style='text-align: left; color: #031B28;'>
                        Advanced Search</h2>""",
                        unsafe_allow_html=True)
    st.sidebar.markdown(
        """
        *Use the sidebar to optionally toggle by season,
        rating, and more.*
        """
    )
    filters = ['Season', 'Episode Rating', 'Speaking Character(s)']
    with st.sidebar:
        selected_filters = st.multiselect(
            "Select which filters to enable",
            filters,
            [],
        )
    seasons = np.unique(df_imdb['Season'])
    characters = np.unique(df_script['Character'])
    ratings = np.unique(df_imdb['averageRating'])
    season_choice = None
    rating_choice = None
    char_choice = None
    if 'Season' in selected_filters:
        season_choice = st.sidebar.multiselect('Select a Season:',
                                               seasons)
    if 'Episode Rating' in selected_filters:
        rating_choice = st.sidebar.slider(
                                'Select which episode ratings to include:',
                                min_value = float(np.min(ratings)),
                                max_value = float(np.max(ratings)),
                                value = (7.1, 9.6))
    if 'Speaking Character(s)' in selected_filters:
        char_choice = st.sidebar.multiselect('Speaking Characters',
                                             characters)
    # Search functionality
    try:
        st.markdown("""<h6 style='text-align: center; color: white;'><br>
                Enter search criteria.</h6>""",
                unsafe_allow_html=True)

        search_string = st.text_input(
            'Enter search criteria: ',
            label_visibility = 'collapsed',
            placeholder = """e.g. Mean soup guy, Jerry and Kramer argue, Kramer falls over""")

        st.markdown("""
            <h6 style='text-align: center; color: white; text-style: italic;'>
            Select an episode to learn more.</h6>""",
            unsafe_allow_html=True)

        # Filter data according to user input
        filtered_df, search_results = episode_query.filter_search_results(
                                                        search_string,
                                                        season_choice,
                                                        rating_choice,
                                                        char_choice,
                                                        df_imdb,
                                                        df_script)
        # Display
        col2_1, col2_2, col2_3 = st.columns([.25, 3.5, .25])
        with col2_2:
            if search_string:
                response = episode_query.get_selected_row(search_results)
            else:
                search_results = filtered_df.sort_values(
                    'averageRating', ascending=False).iloc[:5]
                response = episode_query.get_selected_row(search_results)
        with col2_1 and col2_3:
            pass

        # Descriptive stats
        # Default
        if len(response) == 0:
            desc = 'Choose an episode to view its IMDb description!'
        else:
            selected_imdb = df_imdb[
                df_imdb.Title == response['Title'].values[0]]
            desc = selected_imdb['Description'].values[0]
        # Metadata
        st.markdown("""<h3 style='text-align: left; color: #031B28;'>
                IMDb Episode Description:</h3>""",
                unsafe_allow_html=True)
        st.markdown(desc)
    except RuntimeError:
        st.error("""There was an issue processing your selections for
                    searching functionality."""
                )
    # Analysis functionality
    try:

        if len(response) != 0:

            st.markdown("""<h4 style='text-align: center; color: #031B28;'>
                <br>Average Weighted Sentiment</h4>""",
                unsafe_allow_html=True)

            episode = selected_imdb.Title.values[0]
            selected = episode_query.get_script_from_ep(
                df_imdb, df_script, episode)
            selected[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
                     ] = selected.apply(episode_query.extract_emotions,
                                        axis=1)
            selected['Count'] = 1
            selected['Argmax'] = selected.apply(episode_query.extract_argmax,
                                                axis=1)
            grouped_df = selected[['Happy', 'Angry',
                                   'Surprise', 'Sad',
                                   'Fear', 'SEID']].groupby('SEID').sum()
            grouped_df = grouped_df.reset_index()
            # Melt the DataFrame to create a long format
            melted_df = grouped_df.melt(
                id_vars='SEID',
                var_name='Emotion',
                value_name='sum')

            fig = px.bar(melted_df,
                         x='sum',
                         y='Emotion',
                         color='SEID',
                         orientation='h',
                         template="presentation")

            fig.update_layout(
                xaxis_title="Weighted Total",
                yaxis_title="Sentiment",
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor = "rgba(0,0,0,0)",
                newshape_line_color = "white"
            )
            fig.update_xaxes(
                title_font_color="white",
                tickfont_color="white",
                showgrid=True
            )
            fig.update_yaxes(
                title_font_color="white",
                tickfont_color="white",
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""<h4 style='text-align: center; color: #031B28;'>
                Average Sentiment by Character<br><br></h4>""",
                unsafe_allow_html=True)

            fig2 = px.sunburst(
                selected, path=['Character', 'Argmax'],
                values='Count',
                template="presentation")
            fig2.update_layout(
                width = 500,
                height = 500,
                autosize=True,
                paper_bgcolor="#D4E6FA"
            )

            col3_1, col3_2, col3_3= st.columns([1,6,1])
            with col3_2:
                st.plotly_chart(fig2)
            with col3_1 and col3_3:
                pass

            st.markdown("""<h6 style='text-align: center;
                color: white; font-style: italic;'>
                Click on any characters to see how they were feeling.
                <br><br></h6>""",
                unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(
            """There was an issue processing your data for sentiment analysis.
            Please choose another episode"""
        )
