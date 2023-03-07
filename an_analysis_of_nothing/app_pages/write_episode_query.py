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
import plotly.graph_objects as go
from utils import episode_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def main():
    """
    This function executes the Streamlit formatted HTML
    displayed on the Episode Querying webpage and utilizes user
    inputs to search for and display user input.

    Arguments: None
    Returns: None
    """
    # Intro text/logo
    try:
        # Load data
        df_imdb = pd.DataFrame(st.session_state.df_imdb)
        df_script = pd.DataFrame(st.session_state.df_dialog)
        
        # Titles, image, search bar
        col1_1, col1_2 = st.columns([5, 1])
        with col1_1:
            st.markdown(
                """
                    An Analysis of Nothing: **Episode Querying**
                    ## Find a Seinfeld episode
                """
            )
        with col1_2:
            st.image('./static/images/cast2.png')

        st.markdown(
                """
                Search for specific episodes from the show by entering keywords, 
                concepts, or topics in the search bar below. Then, view sentiment 
                statistics for the five queried episodes.
                """
            )


        col1_3, _ = st.columns([2, 4])
        with col1_3:
            st.image('./static/images/cast_div.png')

    except Exception as e:
        st.error("There was an issue loading data")

    # Configure sidebar
    st.sidebar.markdown("## Advanced Search")
    st.sidebar.markdown(
    """
    *Use the sidebar to optionally toggle by season, 
    rating, and more.*"""
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

    season_choice = None
    rating_choice = None
    char_choice = None

    if 'Season' in selected_filters:
        season_choice = st.sidebar.multiselect('Select a Season:', seasons)

    if 'Episode Rating' in selected_filters:
        ratings = np.unique(df_imdb['averageRating'])
        rating_choice = st.sidebar.slider('Select which episode ratings to include:', 
                                                           min_value = float(np.min(ratings)), 
                                                           max_value = float(np.max(ratings)), 
                                                           value = (7.1, 9.6))
    if 'Speaking Character(s)' in selected_filters:
        characters = np.unique(df_script['Character'])
        char_choice = st.sidebar.multiselect('Speaking Characters', characters)

    # with st.sidebar:
    #     btn = st.button("Reset Filters")
    #     if btn:
    #         season_choice = None
    #         rating_choice = None
    #         char_choice = None

    # Search functionality
    try:
        # Search bar and instructions
        st.markdown('##### Enter search criteria: ')
        search_string = st.text_input(
            'Enter search criteria: ',
            label_visibility = 'collapsed', 
            placeholder = "e.g. Mean soup guy, Jerry and Kramer argue, Kramer falls over")
        st.markdown("""
                    ###### Select an episode to learn more.
                    """
                   )

        # Filter data according to user input
        if season_choice and rating_choice and char_choice:
            filtered_df = util.get_characters(df_imdb, 
                                      df_script, 
                                      char_choice) 
            filtered_df = util.get_ratings(filtered_df, 
                                           rating_choice)
            filtered_df = util.get_seasons(filtered_df, 
                                           season_choice)  
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)

        elif season_choice and rating_choice == None and char_choice == None:        
            filtered_df = util.get_seasons(df_imdb, 
                                           season_choice)
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)

        elif season_choice == None and rating_choice and char_choice == None:        
            filtered_df = util.get_ratings(df_imdb, 
                                           rating_choice)
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)

        elif season_choice == None and rating_choice == None and char_choice:        
            filtered_df = util.get_characters(df_imdb, 
                                              df_script,
                                               char_choice)
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)

        elif season_choice == None and rating_choice and char_choice:     
            filtered_df = util.get_characters(df_imdb, 
                                              df_script,
                                              char_choice)
            filtered_df = util.get_ratings(filtered_df, 
                                            rating_choice)
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)

        elif season_choice and rating_choice == None and char_choice:        
            filtered_df = util.get_seasons(df_imdb, 
                                            season_choice)
            filtered_df = util.get_characters(filtered_df, 
                                              df_script,
                                              char_choice)
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)
        elif season_choice and rating_choice and char_choice == None:        
            filtered_df = util.get_ratings(df_imdb, 
                                            rating_choice)
            filtered_df = util.get_seasons(filtered_df, 
                                              season_choice)
            search_results = util.query_episodes(filtered_df, 
                                                 search_string)
        else:
            filtered_df = df_imdb
            search_results = util.query_episodes(df_imdb, 
                                                 search_string)

        col2_1, col2_2, _, col2_3 = st.columns([4, .5, .5, 2.5])
        with col2_1:
            if search_string:
                response = util.get_selected_row(search_results)
            else:
                search_results = filtered_df.sort_values(
                    'averageRating', ascending=False).iloc[:5]
                response = util.get_selected_row(search_results)

        # Initial descriptive stats
        # Default
        if len(response) == 0:
            desc = 'Choose an episode to view its IMDb description!'
            season = 0
            rating = 0
            director = 'John Doe'
        else:
            selected_imdb = df_imdb[
                df_imdb.Title == response['Title'].values[0]]
            desc = selected_imdb['Description'].values[0]
            season = selected_imdb['Season'].values[0]
            rating = selected_imdb['averageRating'].values[0]
            director = selected_imdb['Director'].values[0]

        # Metadata
        with col2_3:
            st.metric("Season", season)
            st.metric("Average Rating", str(rating) + ' ⭐')
            st.metric("Director", director)     
        st.markdown('###### IMDb Episode Description: ')
        st.markdown(desc)

    except Exception as e:
        st.write(e)
        st.error(
            "There was an issue processing your selections for searching functionality."
        )

    # Analysis functionality
    try:
        st.markdown(
            """
                ### Sentiment Statistics
                Here's a breakdown of that episode's average sentiments. 
            """
        )
        if len(response) != 0:
            episode = selected_imdb.Title.values[0]
            selected = util.get_script_from_ep(
                df_imdb, df_script, episode)

            selected[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
                     ] = selected.apply(util.extract_emotions, axis=1)
            selected['Count'] = 1
            selected['Argmax'] = selected.apply(util.extract_argmax, axis=1)
            grouped_df = selected[['Happy', 'Angry', 'Surprise',
                                   'Sad', 'Fear', 'SEID']].groupby('SEID').sum()
            grouped_df = grouped_df.reset_index()

            # Melt the DataFrame to create a long format
            melted_df = grouped_df.melt(
                id_vars='SEID', var_name='Emotion', value_name='sum')

            fig = px.bar(melted_df, x='sum', y='Emotion',
                         color='SEID', orientation='h')

            fig.update_layout(
                xaxis_title="Weighted Total",
                yaxis_title="Sentiment",
                showlegend=True
            )
            fig2 = px.sunburst(
                selected, path=['Character', 'Argmax'], values='Count')

            col3_1, col3_2, _ = st.columns([3, 3, 1])
            with col3_1:
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('*What emotions prevailed in this episode?*')

            with col3_2:
                st.plotly_chart(fig2)
                st.markdown('*Click on any characters to see how they were feeling.*')
    except Exception as e:
        st.error(
            "There was an issue processing your data for analysis. Please choose another episode"
        )
