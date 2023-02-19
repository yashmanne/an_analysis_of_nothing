# Functional Specification

## Background

The 90s hit, Seinfeld, is an American sitcom that features four friends, Jerry Seinfeld (Jerry Seinfeld), George Costanza (Jason Alexander), Elaine Benes (Julia Louis-Dreyfus), and Cosmo Kramer (Michael Richards), and their daily lives in New York City. The show follows Jerry, a stand-up comedian, and the lives of his best friend, George, his neighbor, Kramer, and his ex-girlfriend, Elaine, all played by real-life comedians. The show has been characterized as a “show about nothing”. While its popularity peaked in the 90s, the show continues to garner new fans along with retaining old ones as it is recognized as one of the most influential sitcoms in TV history.  

Despite the show having cemented its place as one of the greatest sitcoms to date, it can be difficult for Seinfeld fans, as well as those curious about the show, to search and discover certain episode and series characteristics when their only resource is manual web-searching. To this, we develop an interactive web page that covers the extensive capabilities of Wikipedia, IMDb, and Netflix all in one– acting as a descriptive and exploratory tool for users to query specific scenes, visualize character quirks, and receive recommendations for future watches. Via this project development, we hope to not only uncover new insights about the classic show, but also provide a centralized web tool for fans to access and explore all things Seinfeld.

## User Profile

### User #1
- This user is a diehard Seinfeld fan who wants easier searchability for which episode to watch next.
- This user would like to be recommended episodes based on their prior tastes.
- This user wants to be able to search the tool for specific episodes, characters, scenes, lines, etc.
- This user needs a simple user interface that's faster than going to Wikipedia/Netflix etc.
- They also need a high level of detail, since this user is already well-acquainted with Seinfeld.
- This user has an average level of technology skill (is acquainted with similar tools (Google, Wiki, etc.).
- Might prefer a more exploratory user interface (starting with search bar/ recommender).

### User #2
- This user is not familiar with Seinfeld and is curious about episodes, characters, etc.
- The user might like to look at the top 10 ranked episodes, which order to watch, some interesting plot arcs to follow.
- This user needs a simple user interface that's faster than going to Wikipedia/Netflix etc
- They need a guided exploratory interface as they are not well-acquainted with Seinfeld.

### User #3
- This is the NLP expert who will visit the site to perform regular maintenance.
- This user wants to keep the system up to date and make sure there are no bugs. 
- Fine tune the model/features as necessary using additional data from the same set or improve upon the model by introducing new corpora of data.
- Might want more details and transparency about the training data and model building process.

## Data Sources

The data used for this application was downloaded from [Kaggle](https://www.kaggle.com/datasets/thec03u5/seinfeld-chronicles) and scraped from [IMDB](https://www.imdb.com/interfaces/). Both datasets are saved as CSV files and accessed as a dataframe.

## Use Cases

### Episode Recommendation

#### Episode Similarity
Website: Display “Enter/choose your favorite episodes!”.
User: Selects n ranked episode titles in order of favorability.
Could be a text field/auto-fill field or a dropdown menu.
Website: Returns 3 potential episodes to watch based on similarity to prior episodes and 1 that is vastly different.

#### Advanced Character Level: (Episode Recommender with greater search criteria)
Website: Display “Advanced Episode Recommender”.
User: Choose on a dropdown menu which character(s) must be the main focus of the episode.
Website: Returns 3 potential episodes to watch based on similarity to prior episodes and where the focus is the selected character, and 1 that is vastly different.

### Episode Querying

#### General
User: Utilizes the search bar to type in general events/occurrences (X goes to a movie, X fights with Y, etc).
User: Clicks the search button.
Website: Displays a list of episodes that satisfy the query.
User: Click on any episode to learn more (descriptive analytics).

#### Specific
User: Select advanced search option.
User: Input key words in the search bar.
User: Select the season, character, and/or episode rank (range).
User: Click the search button.
Website: Display a list of episodes that fit the user entered criteria (descriptive analytics).

### Descriptive Analytics
Website: List of episodes from general or specific search.
User: Selects an episode of interest.
Website: Returns dashboard of descriptive statistics and visualizations.
User: Filters or toggles descriptive analytics as seen fit.



