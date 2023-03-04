This is our main package.

* `./app/`: contains relevant code for generating a Streamlit application.
* `./tests/`: contains unittests for all package-accessible code.
* `./utils/`: contains relevant modules for application features. This includes:
    * `recommender.py`: module with functions for episode recommendation.
    * `episode_query.py`: module with functions for search functionality.
    * `data_manager.py`: module with functions to parse data for functions including counting number of lines, calculating cumulative sentiment for each group, etc.
    * `data_viz.py`: module with visualization code for Plotly.
