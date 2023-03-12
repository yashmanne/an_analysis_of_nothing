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
    st.markdown("""<h2 style='text-align: center; color: white;'><br>
                        Episode Querying<br><br></h2>""",
                        unsafe_allow_html=True)
    st.markdown("""<h6 style='text-align: left; color: white;'><br>
            Search for specific episodes from the show by entering
            keywords, concepts, or topics in the search bar below.
            Then, view sentiment statistics for the five queried episodes.
            <br><br></h6>""",
            unsafe_allow_html=True)
    left_5, middle_5, right_5 = st.columns([1.65,5,1])
    with middle_5:
        st.image('./static/images/elaine_typing.gif')
    # Configure sidebar
    st.sidebar.markdown("## Advanced Search")
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
        rating_choice = st.sidebar.slider('Select which episode ratings to include:', 
                                           min_value = float(np.min(ratings)),
                                           max_value = float(np.max(ratings)),
                                           value = (7.1, 9.6))
    if 'Speaking Character(s)' in selected_filters:
        char_choice = st.sidebar.multiselect('Speaking Characters',
                                             characters)
    # Search functionality
    try:
        st.markdown('##### Enter search criteria: ')
        search_string = st.text_input(
            'Enter search criteria: ',
            label_visibility = 'collapsed',
            placeholder = """e.g. Mean soup guy, Jerry and Kramer argue, Kramer falls over""")
        st.markdown("""
                    ###### Select an episode to learn more.
                    """
                   )
        # Filter data according to user input
        filtered_df, search_results = episode_query.filter_search_results(
                                                        search_string,
                                                         season_choice,
                                                         rating_choice,
                                                         char_choice,
                                                         df_imdb,
                                                         df_script)
        # Display
        col2_1, col2_2, _, col2_3 = st.columns([4, .5, .5, 2.5])
        with col2_1:
            if search_string:
                response = episode_query.get_selected_row(search_results)
            else:
                search_results = filtered_df.sort_values(
                    'averageRating', ascending=False).iloc[:5]
                response = episode_query.get_selected_row(search_results)
        # Descriptive stats
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
            selected = episode_query.get_script_from_ep(
                df_imdb, df_script, episode)
            selected[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
                     ] = selected.apply(episode_query.extract_emotions,
                                        axis=1)
            selected['Count'] = 1
            selected['Argmax'] = selected.apply(episode_query.extract_argmax,
                                                axis=1)
            grouped_df = selected[['Happy', 'Angry', 'Surprise',
                                   'Sad', 'Fear', 'SEID']].groupby('SEID').sum()
            grouped_df = grouped_df.reset_index()
            # Melt the DataFrame to create a long format
            melted_df = grouped_df.melt(
                id_vars='SEID',
                var_name='Emotion',
                value_name='sum')
            fig = px.bar(melted_df, x='sum', y='Emotion',
                         color='SEID', orientation='h')
            fig.update_layout(
                xaxis_title="Weighted Total",
                yaxis_title="Sentiment",
                showlegend=True
            )
            fig2 = px.sunburst(
                selected, path=['Character', 'Argmax'],
                values='Count')
            col3_1, col3_2, _ = st.columns([3, 3, 1])
            with col3_1:
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('*What emotions prevailed in this episode?*')
            with col3_2:
                st.plotly_chart(fig2)
                st.markdown('*Click on any characters to see how they were feeling.*')
    except Exception as e:
        st.error(
            """There was an issue processing your data for sentiment analysis.
            Please choose another episode"""
        )
