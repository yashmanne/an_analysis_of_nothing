This is our main package. Here is an overview of our structure:

* `./app.py`: main code for creating Streamlit application.
* `requirements.txt`: necessary packages for Streamlit to deploy application.
* `./app_pages/`: contains relevant code for generating pages for Streamlit application.
    * `write_episode_query.py`: page for episode query.
    * `write_recommender.py`: page for episode recommender.
* `./static/`: contains non-code information for the website.
    * `./images/`: contains images used for website.
* `./utils/`: contains relevant modules for application features. This includes:
    * `recommender.py`: module with functions for episode recommendation.
    * `episode_query.py`: module with functions for search functionality.
    * `data_manager.py`: module with functions to parse data for functions including counting number of lines, calculating cumulative sentiment for each group, etc.
    * `data_viz.py`: module with visualization code for Plotly.
* `./tests/`: contains unittests and functional tests for all package-accessible code.
