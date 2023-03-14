# Overview
This is our main package for deploying our web application. 

Here is an overview of our structure:

* `./app.py`: main code for creating Streamlit application. This is **omitted from test coverage** because it is a simple wrapper function calling the files in `./app_pages/`.
* `requirements.txt`: necessary packages for Streamlit to deploy application.
* `./app_pages/`: contains relevant code for generating pages for Streamlit application. Since these files contain predominantly HTML/CSS code, they are **omitted from test coverage**.
  * `write_about_page.py`: about us page.
  * `write_episode_query.py`: page for episode querying.
  * `write_home_page.py`: home page with interactive visual dashboard.
  * `write_recommender_page.py`: page for episode recommender.
* `./static/`: contains non-code information for the website.
  * `./data/`: contains data for subsequent analyses generated through [`../scripts/`](../scripts/README.md).
  * `./images/`: contains images & Gifs used for website.
* `./utils/`: contains relevant modules for application features. This includes:
  * `data_constants`: file containing constants that accessed to load the data in `data_manager.py`.
  * `data_manager.py`: module with functions to parse data for functions including counting number of lines, calculating cumulative sentiment for each group, etc.
  * `episode_query.py`: module with functions for search functionality & advanced filtering options.
    * Predominantly loads precomputed feature vectors for each line of dialogue, computes a feature vector for the search query, and returns the top episodes containing the dialogue lines with the highest cosine similarity with the search query feature vector. 
    * Includes additional functionality to filter search results by season, character, and audience rating.
  * `recommender.py`: module with functions for the episode recommender.
    * Recommends top episodes based on average pairwise cosine similarity between the feature vectors of user's favorite(s) episodes and all other episodes.
    * Multiple feature vectors are calculated using pretrained BERT embeddings for episode dialogue, episode description, episode keywords, and episode summaries. Additional feature vectors include the emotional distribution (# of lines with Anger, Surprise, Fear, Sad, Happy) and the # of lines for the top 20 characters in the show. These feature vectors are individually weighted (proprietary!) and concatenated along one axis to generate a single final feature vector for each episode.
* `./tests/`: contains `unittests` and functional tests for all package-accessible code (primarily those in `./utils/`).
