"""
Code for recommending new episodes.
"""
from typing import List, Union
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from . import data_manager


class Recommender:
    """
    Class to encapsulate recommendation features.
    """

    def __init__(self, meta: pd.DataFrame, scripts: pd.DataFrame,
                 weights: Union[None, List[float]] = None) -> None:
        """
        Initialize recommender with model, data, and feature vectors.
        Note: Takes 1 MIN to initialize
        :param meta: DataFrame with metadata.
            MUST contain these columns: 'Title', 'keyWords', 'Summaries',
            'averageRating', 'numVotes'.
        :param scripts: DataFrame with dialogue data.
            MUST contain these columns: 'SEID', 'Dialogue', 'Happy',
            'Angry', 'Surprise', 'Sad', 'Fear'.
        :param weights: list of floats, relative importance of
            [dialogues, keywords, first summary, average rating,
            numVotes, emotions, number of lines].

        :return: None
        """
        if not isinstance(meta, pd.DataFrame):
            raise TypeError("Argument 'meta' must be a pandas DataFrame")
        if not isinstance(scripts, pd.DataFrame):
            raise TypeError("Argument 'scripts' must be a pandas DataFrame")
        if weights is not None and not isinstance(weights, list):
            raise TypeError("Argument 'weights' must be a list of floats")

        required_columns = ['Title', 'keyWords', 'Summaries', 'averageRating',
                            'numVotes']
        if not all(col in meta.columns for col in required_columns):
            raise ValueError(f"Argument 'meta' must contain columns: "
                             f"{', '.join(required_columns)}")
        required_columns = ['SEID', 'Dialogue', 'Happy', 'Angry', 'Surprise',
                            'Sad', 'Fear']
        if not all(col in scripts.columns for col in required_columns):
            raise ValueError(f"Argument 'scripts' must contain columns: "
                             f"{', '.join(required_columns)}")

        self.meta = meta
        self.scripts = scripts
        self.model = SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2')
        self.default = weights if weights else [1, 1, 0.8, 0.5, 0.2, 0.2, 0.4]
        self.weights = self.default
        self.vector_list = self._generate_vectors()

    @property
    def vectors(self) -> np.array:
        """
        Using property to dynamically update vectors
        whenever self.weights is updated.
        """
        all_features = [self.vector_list[i] * w
                        for i, w in enumerate(self.weights)]
        final_features = np.hstack(all_features)
        return final_features

    def _create_query_vector(self, title_list: list):
        """
        Private function to generate query_vector from input.

        :param title_list: list of strings for each episode name.
                        MUST match episode titles from metadata.csv.

        :return: list of episode indices & np.array of query vector.
        """
        titles = self.meta.Title.to_list()
        ids = [titles.index(title) for title in title_list]

        query_vector = np.stack([self.vectors[i] for i in ids])
        return ids, query_vector

    def _generate_vectors(self):
        """
        Private function to generate feature vectors using features:
        dialogues, keywords, first summary, average rating, numVotes

        :return: np.array of weighted feature vectors
        """
        # each dialog_vector is a unit_norm     31s
        # average feature min, max is -0.11, 0.11
        dialog_vectors = self.model.encode(
            self.scripts.groupby(by='SEID')['Dialogue'].apply('\n'.join))

        # each keyword_vector is a unit_norm    9s
        # average feature min, max is -0.12, 0.12
        keyword_vectors = self.model.encode(
            self.meta.keyWords.apply(" ".join).to_list())

        # each summary_vector is a unit_norm    19s
        # average feature min, max is -0.09, 0.09
        summary_vectors = self.model.encode(
            self.meta.Summaries.apply(lambda x: x[0]).to_list())

        # scale ratings to -0.1, 0.1
        ratings = (MinMaxScaler().fit_transform(
            self.meta.averageRating.values.reshape(-1, 1)) - 0.5) / 5

        # scale num_votes to -0.1, 0.1
        num_votes = (MinMaxScaler().fit_transform(
            self.meta.numVotes.values.reshape(-1, 1)) - 0.5) / 5

        # scale emotions to -0.1, 0.1
        emotions = self.scripts.groupby(by='SEID')[
            ['Happy', 'Angry',
             'Surprise', 'Sad', 'Fear']].apply(np.mean, axis=0).values
        emotions = (MinMaxScaler().fit_transform(emotions) - 0.5) / 5

        # scale line_counts to -0.1, 0.1:
        track_chars = [key for key, value
                       in data_manager.get_line_counts(self.scripts).items()
                       if value > 100]
        track_chars.remove("SETTING")
        track_chars.remove("MAN")
        track_chars.remove("WOMAN")
        char_counts = pd.DataFrame(data_manager.get_line_counts_per_episode(
            self.scripts, track_chars)).values
        char_counts = (MinMaxScaler().fit_transform(char_counts) - 0.5) / 5

        # scale weights
        all_features = [dialog_vectors, keyword_vectors, summary_vectors,
                        ratings, num_votes, emotions, char_counts]
        return all_features

    def find_closest_episodes(self, num_episodes, title_list):
        """
        :param num_episodes: number of episodes to return
        :param title_list: list of strings for each episode name.
                        MUST match episode titles from metadata.csv.

        :return: DataFrame of episode ranked by closeness.
        """
        # Check if num_episodes is a positive integer
        if not isinstance(num_episodes, int) or num_episodes <= 0:
            raise ValueError("num_episodes must be a positive integer.")

        # Check if title_list is a list of strings
        if not isinstance(title_list, list) or not all(
                isinstance(t, str) for t in title_list):
            raise TypeError("title_list must be a list of strings.")

        # Check if all the given episode titles are present in metadata.csv
        if not set(title_list).issubset(set(self.meta['Title'])):
            raise ValueError(
                "One or more episode titles not found in metadata.csv")

        ids, query_vector = self._create_query_vector(title_list)
        scores = -cosine_similarity(query_vector, self.vectors)
        ranked_ids = list(scores.mean(axis=0).argsort())
        for i in ids:
            ranked_ids.remove(i)

        closest_episode_ids = ranked_ids[:num_episodes]
        ranked_episodes = self.meta.iloc[closest_episode_ids]
        return ranked_episodes

    def reset_weights(self):
        """
        Reset weights back to default value.
        """
        self.weights = self.default
