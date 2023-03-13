"""
    Module for testing the data manager.
"""
import unittest
from collections import OrderedDict
from unittest.mock import patch
import pandas as pd
import torch
from utils import data_manager, data_constants


def mocked_read_csv(*args):
    """
        This is a mock function for loading data.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld", "Art Wolff", "S01E01", "tt0098286",
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
        'wine bottle', 'red wine', 'evening', 'audience', 'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones", "S01E02", "tt0697784",
        "The Stakeout", 2, 23, "5113", 7.5, "Jerry and George stake \
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
    ['JERRY', 'Do you know what this is all about? Do you know, why were here? To be out, \
        this is out...and out is one of the single most enjoyable experiences of life. People...\
        did you ever hear people talking about We should go out? This is what theyre talking about...\
        this whole thing, were all out now, no one is home. Not one person here is home, were all out! \
        There are people tryin to find us, they dont know where we are. (on an imaginary phone) Did you ring?, \
        I cant find him. Where did he go? He didnt tell me where he was going. \
        He must have gone out. You wanna go out you get ready, you pick out the clothes, right? You take \
        the shower, you get all ready, get the cash, get your friends, the car, the spot, the reservation..\
        .Then youre standing around, whatta you do? You go We gotta be getting back. Once youre out, \
        you wanna get back! You wanna go to sleep, you wanna get up, you wanna go out again tomorrow, right? \
        Where ever you are in life, its my feeling, youve gotta go.', 'S01E01',
            1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
    ['JERRY', '(pointing at Georges shirt) See, to me, that button is in \
        the worst possible spot. \
        The second button literally makes or breaks the shirt, look at it.\
        Its too high! Its in no-mans-land. \
        You look like you live with your mother.', 'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
    ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
    ['JERRY', 'You do of course try on, when you buy?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 9],
    ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
    ]


    mock_imdb_data = pd.DataFrame(data_imdb_raw, columns=['Season',
        'EpisodeNo', 'AirDate', 'Writers', 'Director', 'SEID', 'tconst',
        'Title', 'EpiNo_Netflix', 'runtimeMinutes', 'numVotes', 'averageRating',
        'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    elif args[0] == data_constants.EPISODE_LINK:
        return mock_imdb_data
    else:
        return mock_imdb_data

def mocked_character_read_csv(*args):
    """
    Mocked data with random new character added.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld", "Art Wolff", "S01E01", "tt0098286",
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
        'wine bottle', 'red wine', 'evening', 'audience', 'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones", "S01E02", "tt0697784",
        "The Stakeout", 2, 23, "5113", 7.5, "Jerry and George stake \
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
    ['JERRY', 'Do you know what this is all about? Do you know, why were here? To be out, \
        this is out...and out is one of the single most enjoyable experiences of life. People...\
        did you ever hear people talking about We should go out? This is what theyre talking about...\
        this whole thing, were all out now, no one is home. Not one person here is home, were all out! \
        There are people tryin to find us, they dont know where we are. (on an imaginary phone) Did you ring?, \
        I cant find him. Where did he go? He didnt tell me where he was going. \
        He must have gone out. You wanna go out you get ready, you pick out the clothes, right? You take \
        the shower, you get all ready, get the cash, get your friends, the car, the spot, the reservation..\
        .Then youre standing around, whatta you do? You go We gotta be getting back. Once youre out, \
        you wanna get back! You wanna go to sleep, you wanna get up, you wanna go out again tomorrow, right? \
        Where ever you are in life, its my feeling, youve gotta go.', 'S01E01',
            1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
    ['JERRY', '(pointing at Georges shirt) See, to me, that button is in \
        the worst possible spot. \
        The second button literally makes or breaks the shirt, look at it.\
        Its too high! Its in no-mans-land. \
        You look like you live with your mother.', 'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
    ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
    ['JERRY & GEORGE', 'You do of course try on, when you buy?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 9],
    ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 3, 0, 0.5, 0, 0.5, 0, 14],
    ['PETER', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 3, 0, 0.5, 0, 0.5, 0, 14],
    ]


    mock_imdb_data = pd.DataFrame(data_imdb_raw, columns=['Season',
        'EpisodeNo', 'AirDate', 'Writers', 'Director', 'SEID', 'tconst',
        'Title', 'EpiNo_Netflix', 'runtimeMinutes', 'numVotes', 'averageRating',
        'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    elif args[0] == data_constants.EPISODE_LINK:
        return mock_imdb_data
    else:
        return mock_imdb_data

class TestDataManager(unittest.TestCase):
    """
    Test class for data manager module
    """
    # Mocking pandas read_csv function
    # def mocked_read_csv(*args, **kwargs):
    #     if args[0] == 'file1.csv':
    #         return pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    #     elif args[0] == 'file2.csv':
    #         return pd.DataFrame({'col1': [4, 5, 6], 'col2': ['d', 'e', 'f']})

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_load_data(self, _):
        """
        Test loading data using mocked data.
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        self.assertIsInstance(imdb, pd.DataFrame)
        self.assertIsInstance(script, pd.DataFrame)

        # Testing that apply eval is working
        self.assertIsInstance(imdb.keyWords.iloc[0], list)
        self.assertIsInstance(imdb.Summaries.iloc[0], list)
        self.assertIsInstance(imdb.keyWords[0][0], str)
        self.assertIsInstance(imdb.Summaries[0][0], str)


        self.assertEqual(len(imdb), 2)
        self.assertEqual(len(script), 5)
        self.assertIsInstance(imdb['Summaries'].iloc[0], list)
        self.assertIsInstance(imdb['keyWords'].iloc[0], list)


    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_line_counts(self, _):
        """
        Smoke test for getting total line counts.
        """
        # mock.return_value = self.mock_imdb_data
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts(script)
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('JERRY', counts)
        self.assertIn('GEORGE', counts)
        self.assertEqual(counts['JERRY'], 3)
        self.assertEqual(counts['GEORGE'], 2)
    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_get_line_counts_per_episode(self, _):
        """
        Smoke test for get line counts per episode.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script)
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('JERRY', counts)
        self.assertEqual(counts['JERRY'].shape, (2,))
        self.assertEqual(counts['JERRY'].tolist(), [3,0])
        self.assertEqual(counts['GEORGE'].tolist(), [1,1])
        self.assertEqual(counts['KRAMER'].tolist(), [0,0])

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_character_read_csv)
    def test_line_counts_per_episode_and(self, _):
        """
        Tests line counts per episdoe with & character splitting.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script)
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('JERRY', counts)
        self.assertEqual(counts['JERRY'].shape, (2,))
        self.assertEqual(counts['JERRY'].tolist(), [3,0])
        self.assertEqual(counts['GEORGE'].tolist(), [2,1])
        self.assertEqual(counts['KRAMER'].tolist(), [0,0])
    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_character_read_csv)
    def test_line_counts_specific(self, _):
        """
        Test for line counts of a specific non-core character.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script, 
            characters=['JERRY', 'PETER'])
        self.assertIsInstance(counts, OrderedDict)

        self.assertIn('PETER', counts)
        self.assertNotIn('GEORGE', counts)
        self.assertEqual(counts['JERRY'].tolist(), [3, 0])
        self.assertEqual(counts['PETER'].tolist(), [0,1])
    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_character_read_csv)
    def test_counts_unkown_specific(self, _):
        """
        Tests when a fake character is passed in character argument.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script,
            characters=['JERRY', 'PETER', 'JABRONI'])
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('PETER', counts)
        self.assertIn('JABRONI', counts)
        self.assertNotIn('GEORGE', counts)
        self.assertEqual(counts['JERRY'].tolist(), [3,0])
        self.assertEqual(counts['PETER'].tolist(), [0, 1])
        self.assertEqual(counts['JABRONI'].tolist(), [0,0])
    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_character_read_csv)
    def test_counts_empty_specific(self, _):
        """
        Test to ensure empty OrderedDict if empty character list is passed.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script, characters=[])
        self.assertIsInstance(counts, OrderedDict)
        self.assertNotIn('GEORGE', counts)
        self.assertEqual(len(counts), 0)


class TestQueryTensor(unittest.TestCase):
    """
    Test class for get_episode_query_tensors()
    """
    # Mocking pandas read_csv function
    # def mocked_read_csv(*args, **kwargs):
    #     if args[0] == 'file1.csv':
    #         return pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    #     elif args[0] == 'file2.csv':
    #         return pd.DataFrame({'col1': [4, 5, 6], 'col2': ['d', 'e', 'f']})

    def setUp(self):
        pass

    def test_smoke(self):
        """
        Smoke test
        """
        tensor = data_manager.get_episode_query_tensors()
        self.assertIsInstance(tensor, torch.Tensor)
        

if __name__ == '__main__':
    unittest.main()
