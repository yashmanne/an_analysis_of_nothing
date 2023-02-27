import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import util


st.set_page_config(layout="wide")
# Intro text and image
try:
    # Load dataframes into session state once
    if "df_imdb" not in st.session_state:
        st.session_state.df_imdb = pd.read_csv('./data/imdb.csv')
    if "df_script" not in st.session_state:
        st.session_state.df_script = pd.read_csv('./data/scripts_emo2.csv')

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.markdown(
            """
                # An Analysis of Nothing
                ### Search Functionality

                Search episodes by keywords, concepts, or topics with the search bar below. Alternatively, choose a couple of your favorite episodes and we will use our proprietary algorithm to suggest some more episodes to watch.
            """
        )

    # Seinfeld image
    with col1_2:
        st.image('./static/images/cast.png')  # use_column_width=True)
except Exception as e:
    st.error("There was an issue loading data")

# Search by phrase and episode recommendation
try:
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        search_string = st.text_input(
            "Search Episodes", placeholder="e.g. Episode with mean soup guy")
        if search_string:
            search_results = util.search_dataframe(
                st.session_state.df_imdb, search_string)
            st.write(search_results[['Title', 'Description',   'Season',
                                    'EpisodeNo', 'averageRating', 'Director', 'Writers']])
        else:
            st.write(st.session_state.df_imdb.sort_values('averageRating', ascending=False).iloc[:5][[
                'Title', 'Description',   'Season', 'EpisodeNo', 'averageRating', 'Director', 'Writers']])
    with col2_2:
        favorite_episodes = st.multiselect(
            'Similar Episodes', st.session_state.df_imdb['Title'].unique())
        # TOOO: change this to a better suggestion algorithm
        if favorite_episodes:
            fav_ep = st.session_state.df_imdb[st.session_state.df_imdb['Title'].isin(
                favorite_episodes)]
            fav_str = ', '.join(
                fav_ep['Summaries'].apply(lambda x: ''.join(x)))

            similar_episodes = util.search_dataframe(
                st.session_state.df_imdb[~st.session_state.df_imdb['Title'].isin(favorite_episodes)], fav_str)
            st.write(similar_episodes)
except Exception as e:
    st.write(e)
    st.error(
        "There was an issue processing your selections for searching functionality.")

# Analysis functionality
try:
    st.markdown(
        """
            ### Analysis Functionality
            Select episodes and see the breakdown of their sentiments by episode as well as the breakdown for each character's dialogue and their sentiments.
        """
    )
    selected_eps = st.multiselect(
        'Episode Analysis', st.session_state.df_imdb['Title'].unique())
    if selected_eps:
        selected = util.get_occurrences(
            st.session_state.df_imdb, st.session_state.df_script, selected_eps)

        # TODO: Make this more efficient by extracting out new columns into original csv
        # TODO: Display weighted sum (i.e. rather than argmax take )
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

        col3_1, col3_2 = st.columns(2)
        with col3_1:
            st.plotly_chart(fig, use_container_width=True)

        with col3_2:
            st.plotly_chart(fig2)
except Exception as e:
    st.error(
        "There was an issue processing your data for analysis. Please choose another episode")
