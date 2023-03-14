# Functional Specification

## Background

The 90s hit, Seinfeld, is an American sitcom that features four friends, Jerry Seinfeld (Jerry Seinfeld), George Costanza (Jason Alexander), Elaine Benes (Julia Louis-Dreyfus), and Cosmo Kramer (Michael Richards), and their daily lives in New York City. The show follows Jerry, a stand-up comedian, and the lives of his best friend, George, his neighbor, Kramer, and his ex-girlfriend, Elaine, all played by real-life comedians. The show has been characterized as a “show about nothing”. While its popularity peaked in the 90s, the show continues to garner new fans along with retaining old ones as it is recognized as one of the most influential sitcoms in TV history.  

Despite the show having cemented its place as one of the greatest sitcoms to date, it can be difficult for Seinfeld fans, as well as those curious about the show, to search and discover certain episode and series characteristics when their only resource is manual web-searching. To this, we develop an interactive web page that covers the extensive capabilities of Wikipedia, IMDb, and Netflix all in one– acting as a descriptive and exploratory tool for users to query specific scenes, visualize character quirks, and receive recommendations for future watches. Via this project development, we hope to not only uncover new insights about the classic show, but also provide a centralized web tool for fans to access and explore all things Seinfeld.

## User Profile

### User #1
- Diehard Seinfeld fan who wants easier searchability for which episode to watch next.
- Wants to receive episode recommendations based on their prior tastes.
- Would like to search the tool for specific episodes, characters, scenes, lines, etc.
- Needs a simple user interface that's faster than Wikipedia/Netflix etc. 
- Prefers a high level of detail, since this user is already well-acquainted with Seinfeld. This includes viewing specific episode insights that they wouldn't already know about the show, such as sentiment statistics. 
- Has an average level of technology skill (is acquainted with similar tools such as Google, Wiki, etc.).
- Might prefer a more exploratory user interface (starting with search bar/ recommender).

### User #2
- Unfamiliar with Seinfeld and is curious about episodes, characters, etc.
- Prefers a low level of detail, since this user has no background knowledge. This includes viewing high level episode insights that they wouldn't already know about the show, such as the top 10 ranked episodes, some interesting plot arcs to follow, and character appearances. 
- Would only use the query tool for broad topics and general plot arcs.
- Needs a simple user interface that's faster than Wikipedia/Netflix etc. 
- Needs a guided exploratory interface as they are not well-acquainted with Seinfeld.

### User #3
- Developer who will visit the site to perform regular maintenance.
- Wants to keep the system up to date and make sure there are no bugs. 
- Fine tune the models and their features as necessary.
- Improve upon the model by introducing new corpora of data or using additional data from the same set.
- Might want more details and transparency about the training data and model building process.

## Data Sources

The data used for this application was downloaded from [Kaggle](https://www.kaggle.com/datasets/thec03u5/seinfeld-chronicles) and scraped from [IMDB](https://www.imdb.com/interfaces/), and contain Seinfeld episode scripts and metadata. Both datasets are saved as CSV files and accessed as a dataframe.

## Use Cases

### General Analysis
1. User: Selects seasons of interest.
2. Website: Displays general analytics like number of lines spoken by main four and episode rating, by season.
3. User: Interacts with and toggles visualizations as seen fit.


### Episode Recommendation
1. Website: Prompts user to enter number of desired recs and favorite episode titles.
2. User: Enters both prompts.
4. Website: Returns n episodes with highest similarity and their metadata via a clickable DataFrame.
5. User: Clicks on an episode.
6. Website: Displays the episode description.

### Episode Querying

#### General
1. User: Utilizes the search bar to type in general events/occurrences (X goes to a movie, X fights with Y, etc).
2. User: Hits enter key on keyboard. 
3. Website: Displays episodes that satisfy the query and their metadata via a clickable DataFrame.
4. User: Clicks on an episode.
5. Website: Displays the episode description and Descriptive Analytics (below).

#### Descriptive Analytics
1. Website: Displays dashboard of descriptive sentiment statistics (consisting of a bar chart and sunburst chart) upon user click.
4. User: Interacts with and toggles descriptive analytics as seen fit.

#### Advanced Search
1. User: Optionally navigates to side bar and selects which filters to apply to search tool.
2. Website: Displays selection box or slider depending on user input.
4. User: Selects the season(s), speaking character(s), and/or episode rating (range).
5. User: Click the search button.
6. Website: Displays episodes that satisfy the query *and* user filters via a clickable DataFrame.





