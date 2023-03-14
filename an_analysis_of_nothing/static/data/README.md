# Data Description
Here is an overview of our data files.

## Table of Contents
* [Metadata](#metadata)
* [Scripts](#scripts)
* [Dialogue Features](#dialogue-features)

<a id="Metadata"></a>
## Metadata
Cleaned metadata for 170 episodes (not including aniversary montage episodes) is stored as `./metadata.csv`. The specific variables available are:
* **Season**: Season number.
* **EpisodeNo**: Episode number (According to Wikipedia).
* **AirDate**: Date of original airing of episode.
* **Writers**: Main writer(s) of episode.
* **Director**: Director of episode.
* **SEID**: Primary key to join with script data.
* **tconst**: Unique IMDb key.
* **Title**: Title of episode.
* **EpiNo_Netflix**: Episode number on Netflix.
* **runtimeMinutes**: Runtime of each episode in minutes.
* **numVotes**: Number of voters of IMDb rating.
* **averageRating**: average IMDb rating for episode.
* **Description**: IMDb-generated episode description
                   (often a snippet of first user summary).
* **Summaries**: user-generated episode summaries on IMDb.
* **keyWords**: IMDb-generated keywords for an episode.

<a id="scripts"></a>
## Scripts
Cleaned data for all 54,590 lines of dialogue in the series is stored as `./scripts.csv`. The specific variables available are:
* **Character**: Speaker of the line. (Can include multiple people or a special designation for `SETTING`).
* **Dialogue**: Spoken dialogue. Can also contain additional actions done by a character in the format `"(<action>) <dialogue>"`.
* **SEID**: Primary key to join with metadata.
* **Season**: Season number.
* **EpisodeNo**: Episode number (According to Wikipedia).
* **Happy**: Overall happiness sentiment of line.
* **Angry**: Overall anger sentiment of line.
* **Surprise**: Overall surprise sentiment of line.
* **Sad**: Overall sadness sentiment of line.
* **Fear**: Overall fear sentiment of line.
* **numWords**: number of whitespace-separated words in dialogue.

<a id="dialogue-features"></a>
## Dialogue Features
The pretrained BERT sentence embeddings for each line of dialogue is originally a 54590x384 Torch `tensor` but was sharded into 10 5459x384 NumPy matrices files that can be rejoined together.
