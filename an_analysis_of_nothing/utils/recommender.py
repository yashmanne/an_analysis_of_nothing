"""
Code for recommending new episodes.
"""

import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


class Recommender:
    """
    Class to encapsulate recommendation features.
    """

    def __init__(self, meta, scripts, weights=None):
        """
        Initialize recommender with model, data, and feature vectors.

        :param meta: DataFrame with metadata.
            MUST contain these columns:
        :param scripts: DataFrame with dialogue data.
            MUST contain these columns:
        :param weights: np.array, relative importance of
            [dialogues, keywords, first summary, average rating, numVotes].

        :return: None
        """
        self.meta = meta
        self.scripts = scripts
        self.model = SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2')
        self.weights = weights if weights else [1, 1, 0.8, 0.5, 0.2]
        self.vectors = self._generate_vectors()

    def _create_query_vector(self, title_list):
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
            self.meta.keyWords.apply(lambda x: " ".join(x)).to_list())

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

        # scale weights
        all_features = [dialog_vectors, keyword_vectors,
                        summary_vectors, ratings, num_votes]
        all_features = [all_features[i] * w for i, w in enumerate(self.weights)]

        final_features = np.hstack(all_features)
        return final_features

    def find_closest_episodes(self, n, title_list):
        """
        :param n: number of episodes to return
        :param title_list: list of strings for each episode name.
                        MUST match episode titles from metadata.csv.

        :return: list of episode indices ranked by closeness.
        """
        ids, query_vector = self._create_query_vector(title_list)
        scores = -cosine_similarity(query_vector, self.vectors)
        ranked_episodes = list(scores.mean(axis=0).argsort())
        for i in ids:
            ranked_episodes.remove(i)

        closest_episode_ids = ranked_episodes[:n]
        return closest_episode_ids
