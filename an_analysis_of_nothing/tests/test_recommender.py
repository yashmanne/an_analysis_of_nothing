"""
    Module for testing the recommender module.
"""

import unittest
from unittest.mock import patch
from utils.recommender import Recommender, data_manager
from . import mock_functions


class TestDataRecommender(unittest.TestCase):
    """
    Test class for the util module recommender.py
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_duplicate)
    def test_init(self, _):
        """
        Tests initiation of recommender.
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        recommender = Recommender(meta=imdb, scripts=script)
        self.assertEqual(recommender.weights, [1, 1, 0.8, 0.5, 0.2, 0.2, 0.4])
        self.assertIsNotNone(recommender.vector_list)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_duplicate)
    def test_finder(self, _):
        """
        Smoke test for finder in recommender.
        """
        imdb, script = data_manager.load_data()
        recommender = Recommender(meta=imdb, scripts=script)
        closest = recommender.find_closest_episodes(1, ['The Stakeout'])
        self.assertEqual(len(closest.Title.tolist()), 1)
        self.assertIsNotNone(closest)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_duplicate)
    def test_finder_exact(self, _):
        """
        Test to make sure it returns episodes with exact same descriptions.
        """
        imdb, script = data_manager.load_data()
        recommender = Recommender(meta=imdb, scripts=script)
        closest = recommender.find_closest_episodes(2, ['The Stakeout'])
        self.assertIsNotNone(closest)
        self.assertIn('The Stakeout2', closest.Title.tolist())
        self.assertIn('The Stakeout3', closest.Title.tolist())

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_duplicate)
    def test_reset(self, _):
        """
        Testing the reset funuction in recommender.
        """
        imdb, script = data_manager.load_data()
        recommender = Recommender(meta=imdb, scripts=script)
        self.assertEqual(recommender.weights, [1, 1, 0.8, 0.5, 0.2, 0.2, 0.4])
        recommender.reset_weights()
        self.assertEqual(recommender.weights, [1, 1, 0.8, 0.5, 0.2, 0.2, 0.4])


class TestDataRecommenderErrors(unittest.TestCase):
    """
    Test class for the util module recommender.py
    """

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_duplicate)
    def test_init_error(self, _):
        """
        Tests initiation of recommender.
        """
        # mock.return_value = self.mock_imdb_data
        imdb, script = data_manager.load_data()
        with self.assertRaises(TypeError):
            Recommender(meta=imdb, scripts='script')
        with self.assertRaises(TypeError):
            Recommender(meta='imdb', scripts=script)
        with self.assertRaises(TypeError):
            Recommender(meta=imdb, scripts=script, weights=5)
        with self.assertRaises(ValueError):
            script2 = script.drop('SEID', axis=1)
            Recommender(meta=imdb, scripts=script2)
        with self.assertRaises(ValueError):
            imdb2 = imdb.drop('Title', axis=1)
            Recommender(meta=imdb2, scripts=script)

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv_duplicate)
    def test_finder(self, _):
        """
        Smoke test for finder in recommender.
        """
        imdb, script = data_manager.load_data()
        recommender = Recommender(meta=imdb, scripts=script)
        with self.assertRaises(ValueError):
            recommender.find_closest_episodes('1', ['The Stakeout'])
        with self.assertRaises(TypeError):
            recommender.find_closest_episodes(1, ['The Stakeout', 5, 3])
        with self.assertRaises(ValueError):
            recommender.find_closest_episodes(1, ['The Jabroni'])
