"""
Define default links for various data sources.

Information:

* `scripts.csv`: Data containing every line of dialogue across 9 seasons.
    * **Character**: speaker of the line. (Can include multiple people or
                     a special designation for `SETTING`).
    * **Dialogue**: Spoken dialogue. Can also contain additional actions done
                    by a character in the format `(<action>) <dialogue>`.
    * **SEID**: Primary key to join with metadata.
    * **Season**: Season number.
    * **EpisodeNo**: Episode number (According to Wikipedia).
    * **Happy**: Overall happiness sentiment of line.
    * **Angry**: Overall anger sentiment of line.
    * **Surprise**: Overall surprise sentiment of line.
    * **Sad**: Overall sadness sentiment of line.
    * **Sad**: Overall sadness sentiment of line.
    * **numWords**: number of whitespace-separated words in dialogue.

* `metadata.csv`: Data providing additional metadata for each episode.
    * **Season**: Season number.
    * **EpisodeNo**: Episode number (According to Wikipedia).
    * **AirDate**: Date of original airing of episode.
    * **Writers**: Main writer(s) of episode.
    * **Director**: Director of episode.
    * **SEID**: Primary key to join with script data.
    * **tconst**: unique IMDb key.
    * **EpiNo_Netflix**: Episode number on Netflix.
    * **runtimeMinutes**: runtime of each episode in minutes.
    * **numVotes**: number of voters of IMDb rating.
    * **averageRating**: average IMDb rating for episode.
    * **Description**: IMDb-generated episode description
                       (often a snippet of first user summary).
    * **Summaries**: user-generated episode summaries on IMDb.
    * **keyWords**: IMDb-generated keyWords for episode.
"""
# Links to Data files
GDRIVE_BASE = 'https://drive.google.com/uc?id='

# Scripts
# pylint: disable=line-too-long
# SCRIPTS_LINK = 'https://drive.google.com/file/d/1zd58WSVxmebSMOMY9zM8myOHqMcKyAX9/view?usp=sharing'
# SCRIPTS_LINK = GDRIVE_BASE + SCRIPTS_LINK.split('/')[-2]
SCRIPTS_LINK = './static/data/scripts.csv'
# Episode Info
# pylint: disable=line-too-long
# EPISODE_LINK = 'https://drive.google.com/file/d/1VA6wa3lc9LnmJSe8I8EtP82Ooc4SQfwz/view?usp=sharing'
# EPISODE_LINK = GDRIVE_BASE + EPISODE_LINK.split('/')[-2]
EPISODE_LINK = './static/data/metadata.csv'
