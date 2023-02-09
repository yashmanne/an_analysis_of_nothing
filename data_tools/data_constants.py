"""
Define default links for various data sources.

scripts.csv: Each character's dialouge for all episodes.
episode_info.csv: Metedata about each episode

Resources:
https://stackoverflow.com/questions/56611698/pandas-how-to-read-csv-file-from-google-drive-public
"""
# Kaggle: https://www.kaggle.com/datasets/thec03u5/seinfeld-chronicles
GDRIVE_BASE = 'https://drive.google.com/uc?id='
# Scripts
SCRIPTS_LINK = 'https://drive.google.com/file/d/19M9N3e-Bp-dwCrxH89XLo_OYMpKw6AtY/view?usp=share_link'
SCRIPTS_LINK = GDRIVE_BASE + SCRIPTS_LINK.split('/')[-2]
# Episode Info
EPISODE_LINK = 'https://drive.google.com/file/d/1Lv6BKNHfE5aSbv0hOkg0FLRolYwVLFdg/view?usp=share_link'
EPISODE_LINK = GDRIVE_BASE + EPISODE_LINK.split('/')[-2]
# IMDb: https://www.imdb.com/interfaces/
SEINFELD_PARENT_TCONST = 'tt0098904'
IMDB_EPISODE = 'https://datasets.imdbws.com/title.episode.tsv.gz'
IMDB_RATING = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
IMDB_BASICS = 'https://datasets.imdbws.com/title.basics.tsv.gz'

# Conversion of Episode Numbers
MAP_IMDB_WIKI = {
    1: {},
    2: {},
    3: {e_num: e_num + 1 for e_num in range(18, 23)},
    4: {},
    5: {},
    6: {e_num: e_num + 1 for e_num in range(15, 24)},
    7: {e_num: e_num + 1 for e_num in range(15, 21)},
    8: {},
    9: {22: 23}
}
MAP_IMDB_WIKI[7].update({e_num: e_num + 2 for e_num in range(21, 23)})
MAP_IMDB_NETFLIX = {
    1: {},
    2: {},
    3: {},
    4: {e_num: e_num - 1 for e_num in range(4, 24)},
    5: {e_num: e_num - 1 for e_num in range(20, 23)},
    6: {},
    7: {},
    8: {},
    9: {}
}
