This folder contains the final, cleaned data files for subsequent analysis.

* `scripts.csv`: Data containing every line of dialogue across 9 seasons.
    * **Character**: speaker of the line. (Can include multiple people or a special designation for `SETTING`).
    * **Dialogue**: Spoken dialogue. Can also contain additional actions done by a character in the format `(<action>) <dialogue>`.
    * **SEID**: Primary key to join with metadata.
    * **Season**: Season number.
    * **EpisodeNo**: Episode number (According to Wikipedia).
    * **Sentiment**: Overall sentiment of line.
* `meta.csv`: Data providing additional metadata for each episode.
    * **Season**: Season number.
    * **EpisodeNo**: Episode number (According to Wikipedia).
    * **AirDate**: Date of orignal airing of episode.
    * **Writers**: Main writer(s) of episode.
    * **Director**: Director of episode.
    * **SEID**: Primary key to join with script data.
    * **tconst**: unique IMDb key.
    * **EpiNo_Netflix**: Episode number on Netflix.
    * **runtimeMinutes**: runtime of each episode in minutes.
    * **numVotes**: number of voters of IMDb rating.
    * **averageRating**: average IMDb rating for episode.
    * **Description**: IMDb-generated episode description (often a snippet of first user summary).
    * **Summaries**: user-generated epsiode summaries on IMDb.
    * **keyWords**: IMDb-generated keyWords for episode.
