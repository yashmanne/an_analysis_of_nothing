"""
Define default links for various data sources.

scripts.csv: Each character's dialouge for all episodes.
episode_info.csv: Metedata about each episode

Resources:
https://stackoverflow.com/questions/56611698/pandas-how-to-read-csv-file-from-google-drive-public
"""
# Links to Data files
GDRIVE_BASE = 'https://drive.google.com/uc?id='
# Cached on 2/19/23
# pylint: disable=line-too-long
PROCESSED_SCRIPTS = ''
# pylint: disable=line-too-long
PROCESSED_METADATA = ''

# Kaggle: https://www.kaggle.com/datasets/thec03u5/seinfeld-chronicles
# Scripts
# pylint: disable=line-too-long
SCRIPTS_LINK = 'https://drive.google.com/file/d/19M9N3e-Bp-dwCrxH89XLo_OYMpKw6AtY/view?usp=share_link'
SCRIPTS_LINK = GDRIVE_BASE + SCRIPTS_LINK.split('/')[-2]
# Episode Info
# pylint: disable=line-too-long
EPISODE_LINK = 'https://drive.google.com/file/d/1Lv6BKNHfE5aSbv0hOkg0FLRolYwVLFdg/view?usp=share_link'
EPISODE_LINK = GDRIVE_BASE + EPISODE_LINK.split('/')[-2]
# IMDb: https://www.imdb.com/interfaces/
SEINFELD_PARENT_TCONST = 'tt0098904'
IMDB_EPISODE = 'https://datasets.imdbws.com/title.episode.tsv.gz'
IMDB_RATING = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
IMDB_BASICS = 'https://datasets.imdbws.com/title.basics.tsv.gz'
# IMDb Summaries & Keywords
# pylint: disable=line-too-long
IMDB_SUMMARIES = 'https://drive.google.com/file/d/1HNucKvxfsvWrSQx58spDwPpkzfPfYo5u/view?usp=share_link'
IMDB_SUMMARIES = GDRIVE_BASE + IMDB_SUMMARIES.split('/')[-2]
# Defining Constants For Scraping Summaries & Keywords
IMDB_DESC = 'https://www.imdb.com/title/tt0098904/episodes?season={szn}'
IMDB_SUMMARY = 'https://www.imdb.com/title/{tconst}/plotsummary'
IMDB_KWORDS = 'https://www.imdb.com/title/{tconst}/keywords'
HDR = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
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

if __name__ == '__main__':
    pass
