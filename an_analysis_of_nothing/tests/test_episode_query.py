"""
Contains tests for episode querying.
Specifically, the tests will extract:
    * Filter Search Results
    * Load Corpus
    * Query Episodes
    * Get Selected Row
    * Get Characters
    * Get Seasons
    * Get Ratings
    * Get Script from Episode
    * Extract Emotions
    * Extract Argument Max
"""

import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
import torch
from utils import data_manager, episode_query
from . import mock_functions


class MockObject:
    """
    Object mocking st.session_state
    """

    def __init__(self):
        pass

    def __getattr__(self, name):
        if name == 'query':
            return load_corpus()
        return ''

    def print(self):
        """
        Print the class name
        """
        print('MockObject')


def load_corpus():
    """
    This function loads a corpus for testing.
    :return:    list: Dialogue and summaries for each episode in df_imdb.
                tensor: Vectorized corpus (embeddings).
                SentenceTransformer: BertModel for finding closest matches.
    """
    _, script = data_manager.load_data()
    return episode_query.load_corpus(script)


class TestGetScriptFromEp(unittest.TestCase):
    """
    Test class for testing get_script_from_ep() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for getting script from episode list
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        selected_dialogue = episode_query.get_script_from_ep(
            imdb, script, "Good News, Bad News")
        self.assertIn('S01E01', selected_dialogue.SEID.unique())
        self.assertEqual(len(selected_dialogue), 3)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_fake_episode(self, _):
        """
        Smoke test for getting script from episode list
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        selected_dialogue = episode_query.get_script_from_ep(
            imdb, script, "Good Bad News")
        self.assertEqual(len(selected_dialogue), 0)

    # @patch('utils.data_manager.pd.read_csv',
    #        side_effect=mock_functions.mocked_read_csv_query)
    # def test_error(self, _):
    #     """
    #     Smoke test for getting script from episode list
    #     """
    #     # mock.return_value = self.mock_imdb_data
    #     imdb, script = data_manager.load_data()
    #     imdb = 3
    #     selected_dialogue = episode_query.get_script_from_ep(
    #         imdb, script, "Good Bad News")
    #     pd.testing.assert_frame_equal(selected_dialogue, script)


class TestGetRatings(unittest.TestCase):
    """
    Test class for the get_ratings() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for getting script from episode list
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (5, 9))
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_small_range(self, _):
        """
        Tests a smaller range where 1 result won't be included
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (7, 8))
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 1)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_out_range(self, _):
        """
        Tests when no results in range
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (2, 3))
        self.assertNotIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 0)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_zero_range(self, _):
        """
        Tests when range starts and ends with the same number
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (7.4, 7.4))
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 1)


class TestGetSeasons(unittest.TestCase):
    """
    Test class for the get_seasons() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for getting script from episode list
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_seasons(imdb, [1])
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_multiple_seasons(self, _):
        """
        Tests for multiple season numbers
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_seasons(imdb, [1, 2])
        self.assertIn('S02E02', eps.SEID.unique())
        self.assertEqual(len(eps), 3)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_nonexistent_season(self, _):
        """
        Tests for multiple season numbers
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_seasons(imdb, [100, 101])
        self.assertNotIn('S02E02', eps.SEID.unique())
        self.assertEqual(len(eps), 0)


class TestExtractEmotion(unittest.TestCase):
    """
    Test class for the extract_emotions() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for emotion extraction
        """
        _, script = data_manager.load_data()
        emotions = episode_query.extract_emotions(script.iloc[0, :])
        groud_truth = pd.Series({'Happy': .24,
                                 'Angry': 0,
                                 'Surprise': 0,
                                 'Sad': .41,
                                 'Fear': .35})
        self.assertIsInstance(emotions, pd.Series)
        pd.testing.assert_series_equal(emotions, groud_truth)


class TestExtractArgmax(unittest.TestCase):
    """
    Test class for the extract_argmax() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for argmax extraction
        """
        _, script = data_manager.load_data()
        emotion = episode_query.extract_argmax(script.iloc[0, :])
        self.assertIsInstance(emotion, str)

        self.assertEqual(emotion, 'Sad')

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_no_emotion(self, _):
        """
        Tests no emotion
        """
        _, script = data_manager.load_data()
        script.iloc[0, 5:10] = 0
        emotion = episode_query.extract_argmax(script.iloc[0, :])
        self.assertIsInstance(emotion, str)
        self.assertEqual(emotion, 'No Emotion')


class TestGetCharacters(unittest.TestCase):
    """
    Test class for the get_characters() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for get characters
        """
        imdb, script = data_manager.load_data()
        eps = episode_query.get_characters(imdb, script, ['JERRY'])
        self.assertIn('S01E02', eps.SEID.tolist())
        self.assertEqual(len(eps.SEID.tolist()), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_multiple_characters(self, _):
        """
        Tests passing multiple characters.
        """
        imdb, script = data_manager.load_data()
        eps = episode_query.get_characters(imdb, script, ['JERRY', 'GEORGE'])
        self.assertIn('S01E02', eps.SEID.tolist())
        self.assertEqual(len(eps.SEID.tolist()), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_fake_characters(self, _):
        """
        Tests passing multiple characters.
        """
        imdb, script = data_manager.load_data()
        eps = episode_query.get_characters(imdb, script, ['JIMBO', 'JABRONI'])
        self.assertNotIn('S01E02', eps.SEID.tolist())
        self.assertEqual(len(eps.SEID.tolist()), 0)


class TestLoadCorpus(unittest.TestCase):
    """
    Test class for the load_corpus() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_query)
    def test_smoke(self, _):
        """
        Smoke test for load corpus
        """
        _, script = data_manager.load_data()
        c_object, c_emb, _ = episode_query.load_corpus(script)

        self.assertIsInstance(c_object, object)
        self.assertIsInstance(c_emb, torch.Tensor)


class TestFilterSearchResults(unittest.TestCase):
    """
    Test class for the filter_search_results() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_all_values(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = [1]
        rating_choice = [7, 10]
        char_choice = ['JERRY']
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertEqual(True, filtered_df.iloc[0]['char_check'])
        self.assertEqual(1, filtered_df.iloc[0]['Season'])
        self.assertGreater(np.min(filtered_df['averageRating']), 6.9)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_rating_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = [1]
        rating_choice = None
        char_choice = ['JERRY']
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertEqual(True, filtered_df.iloc[0]['char_check'])
        self.assertNotIn(2, filtered_df['Season'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 1)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_rating_char_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = [1]
        rating_choice = None
        char_choice = None
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertNotIn(4, filtered_df['Season'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_season_char_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = None
        rating_choice = [8, 10]
        char_choice = None
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertIn(4, filtered_df['Season'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_season_rating_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = None
        rating_choice = None
        char_choice = ['KRAMER']
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertIn(2, filtered_df['EpisodeNo'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 1)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_season_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = None
        rating_choice = [8, 8.5]
        char_choice = ['GEORGE']
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertIn(4, filtered_df['Season'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 1)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_char_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = [1, 4]
        rating_choice = [8, 9]
        char_choice = None
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertIn(1, filtered_df['Season'].tolist())
        self.assertIn(4, filtered_df['Season'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 2)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_all_none(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = None
        rating_choice = None
        char_choice = None
        filtered_df, _ = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        self.assertIn(1, filtered_df['Season'].tolist())
        self.assertIn(2, filtered_df['EpisodeNo'].tolist())
        self.assertIn(4, filtered_df['Season'].tolist())
        self.assertEqual(len(filtered_df['averageRating']), 3)
        pd.testing.assert_frame_equal(filtered_df, imdb)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_large)
    @patch('streamlit.session_state', MockObject())
    def test_get_selected_row(self, _):
        """
        Tests when non of arguments are null
        """
        imdb, script = data_manager.load_data()
        search_string = "Jerry waits in lobby"
        season_choice = None
        rating_choice = None
        char_choice = None
        _, search_results = episode_query.filter_search_results(
            search_string, season_choice, rating_choice,
            char_choice, imdb, script)
        rows = episode_query.get_selected_row(search_results)
        self.assertIsInstance(rows, pd.DataFrame)
