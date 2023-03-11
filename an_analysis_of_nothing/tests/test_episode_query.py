import unittest
from utils import data_manager, episode_query
import pandas as pd
from unittest.mock import patch, MagicMock


def mocked_read_csv(*args, **kwargs):
        data_imdb_raw = [
            [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld", "Art Wolff", "S01E01", "tt0098286", "Good News, Bad News", 1, 23, "6031", 7.4, "Jerry and George argue whether an overnight visitor Jerry is expecting is coming with romantic intentions. ", """["In this episode, the predecessor to Seinfeld (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York. Throughout the first part of the show Jerry and George are discussing the situation. Later we meet 'Kessler' who comes in to Jerry\'s apartment to borrow some meat and uncharacteristically knocks on the door before entering."]""", "['tv series pilot', 'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport', 'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', 'laundromat', 'romantic interest', 'realtor', 'overnight', 'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', 'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer', 'refrigerator', 'sandwich', 'sitting on a couch', 'eating cereal', 'cereal', 'magazine', 'waiting', 'surprise', 'handshake', 'luggage', 'help', 'relaxation', 'hospitality', 'lap', 'man takes off shoes', 'wine bottle', 'red wine', 'evening', 'audience', 'watching sports on tv', 'microphone in shot', 'club', 'excitement', 'observational comedy', 'caffeine effect', 'intelligent woman', 'bachelor', 'eating', 'opening a can', 'drink', 'drinking', 'given a drink', 'drinking together', 'bald man', 'comedian', 'dartboard', 'blonde woman', 'woman on the phone', 'couch', 'listening to phone conversation', 'sports equipment', 'short haired woman', 'talking into a microphone', 'microphone', 'eating a sandwich', 'man eating', 'food', 'meat sandwich', 'nightgown', 'unshaved', 'drinking coffee', 'friends talking', 'argument', 'overnight guest', 'expectation', 'visit', 'discussion', 'discussing a problem', 'borrowing meat', 'knocking on a door', 'dryer', 'stand up comedy', 'stand up comedian', 'stage', 'cafeteria', 'baldness', 'boredom', 'happiness', 'laughter', 'man wears eyeglasses', 'neighbor', 'telephone', 'telephone call', 'fiance fiancee relationship', 'famous entrance', 'pilot episode with missing cast']"],
            [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones", "S01E02", "tt0697784", "The Stakeout", 2, 23, "5113", 7.5, "Jerry and George stake out the lobby of an office building to find a woman Jerry met at a party but whose name and phone number he didn't get.", """["Elaine drags Jerry to a birthday dinner for one of her friends where he meets an attractive woman. He promptly forgets her name and refuses to ask Elaine who she is but remembers where she works. Jerry's parents are in town to go to a family wedding and his Dad suggests he stake-out the lobby around lunchtime. George tags along but they can't quite seem to get their stories straight. Elaine hears about it making them both uncomfortable."]""", "['reference to loni anderson', 'pornography', 'fake name', 'scrabble', 'hearing characters thoughts', 'made up word', 'reference to john cougar mellencamp', 'reference to ethel merman', 'polishing shoes', 'birthday party', 'dream', 'video store']"],
        ]
        data_scripts_raw = [
            ['JERRY', 'Do you know what this is all about? Do you know, why were here? To be out, this is out...and out is one of the single most enjoyable experiences of life. People...did you ever hear people talking about We should go out? This is what theyre talking about...this whole thing, were all out now, no one is home. Not one person here is home, were all out! There are people tryin to find us, they dont know where we are. (on an imaginary phone) Did you ring?, I cant find him. Where did he go? He didnt tell me where he was going. He must have gone out. You wanna go out you get ready, you pick out the clothes, right? You take the shower, you get all ready, get the cash, get your friends, the car, the spot, the reservation...Then youre standing around, whatta you do? You go We gotta be getting back. Once youre out, you wanna get back! You wanna go to sleep, you wanna get up, you wanna go out again tomorrow, right? Where ever you are in life, its my feeling, youve gotta go.', 'S01E01', 1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
            ['JERRY', '(pointing at Georges shirt) See, to me, that button is in the worst possible spot. The second button literally makes or breaks the shirt, look at it. Its too high! Its in no-mans-land. You look like you live with your mother.', 'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
            ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
            ['JERRY', 'You do of course try on, when you buy?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 9],
            ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall considering the buttons.', 'S01E01', 1, 1, 0, 0.5, 0, 0.5, 0, 14]
        ]


        mock_imdb_data = pd.DataFrame(data_imdb_raw, columns=['Season', 'EpisodeNo', 'AirDate', 'Writers', 'Director', 'SEID', 'tconst', 'Title', 'EpiNo_Netflix', 'runtimeMinutes', 'numVotes', 'averageRating', 'Description', 'Summaries', 'keyWords'])
        mock_script_data = pd.DataFrame(data_scripts_raw, columns=['Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo', 'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])
       
        if args[0] == 'https://drive.google.com/uc?id=1VA6wa3lc9LnmJSe8I8EtP82Ooc4SQfwz': #episode link
            return mock_imdb_data
        elif args[0] == 'https://drive.google.com/uc?id=1zd58WSVxmebSMOMY9zM8myOHqMcKyAX9':
            return mock_script_data

class TestEpisodeQuery(unittest.TestCase):
    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_query_episodes(self, mock):
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        episodes = episode_query.query_episodes(imdb, 'Woman from michigan')
        pd.testing.assert_frame_equal(episodes, imdb)

        episodes = episode_query.query_episodes(imdb, 'Jerry goes to a birthday party')
        pd.testing.assert_frame_equal(episodes, imdb)
    
    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_query_episodes_error(self, mock):
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        imdb.rename(columns={"Summaries": "summaries"})
        episodes = episode_query.query_episodes(imdb, 'Woman from michigan')
        pd.testing.assert_frame_equal(episodes, imdb)

    @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv)
    def test_query_episodes_ag_obj(self, mock):
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        episodes = episode_query.query_episodes(imdb, 'Woman from michigan')  
        ag_obj = episode_query.get_selected_row(episodes)
        print(ag_obj)
        self.assertIsInstance(ag_obj, pd.DataFrame)
    
    # @patch('utils.data_manager.pd.read_csv', side_effect=mocked_read_csv) # this is unnecessary function
    # def test_transform(self, mock):
    #     # mock.return_value = self.mock_imdb_data
    #     imdb, script = data_manager.load_data()
    #     new_imdb = episode_query.map_imdb_to_scripts(imdb, script)
    #     self.assertIn('SEID', new_imdb.columns)
