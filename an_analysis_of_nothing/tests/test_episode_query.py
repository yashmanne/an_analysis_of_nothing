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
from utils import data_manager, episode_query, data_constants


class MockObject:
    """
    Object mocking st.session_state
    """

    def __init__(self):
        pass

    def __getattr__(self, name):
        if name == 'query':
            return load_corpus()


def load_corpus():
    """
    This function loads a corpus for testing.
    :return:    list: Dialogue and summaries for each episode in df_imdb.
                tensor: Vectorized corpus (embeddings).
                SentenceTransformer: BertModel for finding closest matches.
    """
    imdb, script = data_manager.load_data()
    return episode_query.load_corpus(imdb, script)


def mocked_read_csv(*args):
    """
        This function mocks pd.read_csv and return either scripts
        or imdb dataframes.
        :return: Pandas Dataframe
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
         "Art Wolff", "S01E01", "tt0098286",
         "Good News, Bad News", 1, 23, "6031", 7.4,
         "Jerry and George argue \
        whether an overnight visitor \
        Jerry is expecting is coming with romantic intentions. ", """["In \
        this episode, the predecessor to Seinfeld \
        (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York.\
        Throughout the first part of the show Jerry and \
        George are discussing the situation. Later we meet 'Kessler' \
        who comes in to Jerry\'s apartment to borrow some \
        meat and uncharacteristically \
        knocks on the door before entering."]""", "['tv series pilot', \
        'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport',\
        'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', \
        'laundromat', 'romantic interest', 'realtor', 'overnight', \
        'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', \
        'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer',\
        'refrigerator', \
        'sandwich', 'sitting on a couch', 'eating cereal', \
        'cereal', 'magazine', 'waiting', 'surprise', 'handshake', \
        'luggage', 'help', 'relaxation', 'hospitality', 'lap', 'man takes off shoes', \
        'wine bottle', 'red wine', 'evening', \
        'audience', 'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 9, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],

        [2, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones",
         "S02E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 1, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],
    ]
    data_scripts_raw = [
        ['JERRY', 'Do you know what this is all about?\
         Do you know, why were here? To be out, \
        this is out...and out is one of the single most enjoyable \
            experiences of life. People...\
        did you ever hear people talking about We should go out?\
        This is what theyre talking about...\
        this whole thing, were all out now, no one is home. Not one \
        person here is home, were all out! \
        There are people tryin to find us, they dont know \
        where we are. (on an imaginary phone) Did you ring?, \
        I cant find him. Where did he go? He didnt tell me where he was going. \
        He must have gone out. You wanna go out you get ready, \
        you pick out the clothes, right? You take \
        the shower, you get all ready, get the cash, \
        get your friends, the car, the spot, the reservation..\
        .Then youre standing around, whatta you do? You go \
        We gotta be getting back. Once youre out, \
        you wanna get back! You wanna go to sleep, you wanna get up, \
        you wanna go out again tomorrow, right? \
        Where ever you are in life, its my feeling, youve gotta go.',
         'S01E01',
         1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
        ['JERRY', '(pointing at Georges shirt) See, to me, that button is in \
        the worst possible spot. \
        The second button literally makes or breaks the shirt, look at it.\
        Its too high! Its in no-mans-land. \
        You look like you live with your mother.',
         'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['JERRY', 'You do of course try on, when you buy?',
            'S01E02', 1, 1, 0, 0, 0, 0, 0, 9],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
    ]

    mock_imdb_data = pd.DataFrame(
        data_imdb_raw, columns=['Season',
                                'EpisodeNo', 'AirDate', 'Writers',
                                'Director', 'SEID', 'tconst',
                                'Title', 'EpiNo_Netflix', 'runtimeMinutes',
                                'numVotes', 'averageRating',
                                'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data


def mocked_read_csv_large(*args):
    """
        This is a mock function for loading data.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
         "Art Wolff", "S01E01", "tt0098286",
         "Good News, Bad News", 1, 23, "6031", 7.4, "Jerry and George argue \
        whether an overnight visitor \
        Jerry is expecting is coming with romantic intentions. ", """["In \
        this episode, the predecessor to Seinfeld \
        (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York.\
        Throughout the first part of the show Jerry and \
        George are discussing the situation. Later we meet 'Kessler' \
        who comes in to Jerry\'s apartment to borrow some \
        meat and uncharacteristically \
        knocks on the door before entering."]""", "['tv series pilot', \
        'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport',\
        'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', \
        'laundromat', 'romantic interest', 'realtor', 'overnight', \
        'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', \
        'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer',\
        'refrigerator', \
        'sandwich', 'sitting on a couch', 'eating cereal', \
        'cereal', 'magazine', 'waiting', 'surprise', 'handshake', \
        'luggage', 'help', 'relaxation', 'hospitality', 'lap', 'man takes off shoes', \
        'wine bottle', 'red wine', 'evening', 'audience',\
        'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 9, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],

        [4, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones",
         "S04E02", "tt0697784",
         "The Stakeout", 4, 23, "5113", 8, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],
    ]
    data_scripts_raw = [
        ['JERRY', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['KRAMER', 'Are you through?', 'S01E02', 1, 2, 0, 0, 0, 0, 0, 3],
        ['GEORGE', 'Are you through?', 'S04E02', 4, 2, 0, 0, 0, 0, 0, 3],
    ] * 50000

    mock_imdb_data = pd.DataFrame(
        data_imdb_raw, columns=['Season',
                                'EpisodeNo', 'AirDate', 'Writers',
                                'Director', 'SEID', 'tconst',
                                'Title', 'EpiNo_Netflix', 'runtimeMinutes',
                                'numVotes', 'averageRating',
                                'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data


class TestGetScriptFromEp(unittest.TestCase):
    """
    Test class for testing get_script_from_ep() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_fake_episode(self, _):
        """
        Smoke test for getting script from episode list
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        selected_dialogue = episode_query.get_script_from_ep(
            imdb, script, "Good Bad News")
        self.assertEqual(len(selected_dialogue), 0)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_error(self, _):
        """
        Smoke test for getting script from episode list
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        imdb = 3
        selected_dialogue = episode_query.get_script_from_ep(
            imdb, script, "Good Bad News")
        pd.testing.assert_frame_equal(selected_dialogue, script)


class TestGetRatings(unittest.TestCase):
    """
    Test class for the get_ratings() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_smoke(self, _):
        """
        Smoke test for getting script from episode list
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (5, 9))
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 2)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_small_range(self, _):
        """
        Tests a smaller range where 1 result won't be included
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (7, 8))
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 1)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_out_range(self, _):
        """
        Tests when no results in range
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_ratings(imdb, (2, 3))
        self.assertNotIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 0)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_smoke(self, _):
        """
        Smoke test for getting script from episode list
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_seasons(imdb, [1])
        self.assertIn('S01E01', eps.SEID.unique())
        self.assertEqual(len(eps), 2)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_multiple_seasons(self, _):
        """
        Tests for multiple season numbers
        """
        imdb, _ = data_manager.load_data()
        eps = episode_query.get_seasons(imdb, [1, 2])
        self.assertIn('S02E02', eps.SEID.unique())
        self.assertEqual(len(eps), 3)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_smoke(self, _):
        """
        Smoke test for argmax extraction
        """
        _, script = data_manager.load_data()
        emotion = episode_query.extract_argmax(script.iloc[0, :])
        self.assertIsInstance(emotion, str)

        self.assertEqual(emotion, 'Sad')

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_smoke(self, _):
        """
        Smoke test for get characters
        """
        imdb, script = data_manager.load_data()
        eps = episode_query.get_characters(imdb, script, ['JERRY'])
        self.assertIn('S01E02', eps.SEID.tolist())
        self.assertEqual(len(eps.SEID.tolist()), 2)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_multiple_characters(self, _):
        """
        Tests passing multiple characters.
        """
        imdb, script = data_manager.load_data()
        eps = episode_query.get_characters(imdb, script, ['JERRY', 'GEORGE'])
        self.assertIn('S01E02', eps.SEID.tolist())
        self.assertEqual(len(eps.SEID.tolist()), 2)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_smoke(self, _):
        """
        Smoke test for load corpus
        """
        imdb, script = data_manager.load_data()
        c_object, c_emb, _ = episode_query.load_corpus(imdb, script)

        self.assertIsInstance(c_object, object)
        self.assertIsInstance(c_emb, torch.Tensor)


class TestFilterSearchResults(unittest.TestCase):
    """
    Test class for the filter_search_results() method
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv_large)
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
