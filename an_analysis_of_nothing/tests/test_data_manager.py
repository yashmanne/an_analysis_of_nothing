"""
    Module for testing the data manager.
"""
import unittest
from collections import OrderedDict
from unittest.mock import patch
import pandas as pd
import torch
from utils import data_manager
from . import mock_functions


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

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv)
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

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv)
    def test_get_line_counts_per_episode(self, _):
        """
        Smoke test for get line counts per episode.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script)
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('JERRY', counts)
        self.assertEqual(counts['JERRY'].shape, (2,))
        self.assertEqual(counts['JERRY'].tolist(), [3, 0])
        self.assertEqual(counts['GEORGE'].tolist(), [1, 1])
        self.assertEqual(counts['KRAMER'].tolist(), [0, 0])

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_character_read_csv)
    def test_line_counts_per_episode_and(self, _):
        """
        Tests line counts per episdoe with & character splitting.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(scripts=script)
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('JERRY', counts)
        self.assertEqual(counts['JERRY'].shape, (2,))
        self.assertEqual(counts['JERRY'].tolist(), [3, 0])
        self.assertEqual(counts['GEORGE'].tolist(), [2, 1])
        self.assertEqual(counts['KRAMER'].tolist(), [0, 0])

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_character_read_csv)
    def test_line_counts_specific(self, _):
        """
        Test for line counts of a specific non-core character.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(
            scripts=script, characters=['JERRY', 'PETER'])
        self.assertIsInstance(counts, OrderedDict)

        self.assertIn('PETER', counts)
        self.assertNotIn('GEORGE', counts)
        self.assertEqual(counts['JERRY'].tolist(), [3, 0])
        self.assertEqual(counts['PETER'].tolist(), [0, 1])

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_character_read_csv)
    def test_counts_unkown_specific(self, _):
        """
        Tests when a fake character is passed in character argument.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(
            scripts=script, characters=['JERRY', 'PETER', 'JABRONI'])
        self.assertIsInstance(counts, OrderedDict)
        self.assertIn('PETER', counts)
        self.assertIn('JABRONI', counts)
        self.assertNotIn('GEORGE', counts)
        self.assertEqual(counts['JERRY'].tolist(), [3, 0])
        self.assertEqual(counts['PETER'].tolist(), [0, 1])
        self.assertEqual(counts['JABRONI'].tolist(), [0, 0])

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_character_read_csv)
    def test_counts_empty_specific(self, _):
        """
        Test to ensure empty OrderedDict if empty character list is passed.
        """
        _, script = data_manager.load_data()
        counts = data_manager.get_line_counts_per_episode(
            scripts=script, characters=[])
        self.assertIsInstance(counts, OrderedDict)
        self.assertNotIn('GEORGE', counts)
        self.assertEqual(len(counts), 0)


class TestQueryTensor(unittest.TestCase):
    """
    Test class for get_episode_query_tensors()
    """

    def setUp(self):
        pass

    def test_smoke(self):
        """
        Smoke test
        """
        tensor = data_manager.get_episode_query_tensors()
        self.assertIsInstance(tensor, torch.Tensor)


class TestDataManagerErrors(unittest.TestCase):
    """
    Test class for testing data manager module error handling
    """
    # Mocking pandas read_csv function
    # def mocked_read_csv(*args, **kwargs):
    #     if args[0] == 'file1.csv':
    #         return pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    #     elif args[0] == 'file2.csv':
    #         return pd.DataFrame({'col1': [4, 5, 6], 'col2': ['d', 'e', 'f']})

    def setUp(self):
        pass

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv)
    def test_get_tensor(self, _):
        """
        Test loading data using mocked data.
        """
        with self.assertRaises(TypeError):
            data_manager.get_episode_query_tensors('ten')

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv)
    def test_line_counts(self, _):
        """
        Test loading data using mocked data.
        """
        with self.assertRaises(TypeError):
            data_manager.get_line_counts(['one', 'two', 'three'])

    @patch('utils.data_manager.pd.read_csv',
           side_effect=mock_functions.mocked_read_csv)
    def test_line_counts_episode(self, _):
        """
        Test loading data using mocked data.
        """
        _, script = data_manager.load_data()

        with self.assertRaises(TypeError):
            data_manager.get_line_counts_per_episode(script, 'kramer')

        with self.assertRaises(TypeError):
            data_manager.get_line_counts_per_episode('script', ['kramer'])
