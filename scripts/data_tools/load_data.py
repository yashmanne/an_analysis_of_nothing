"""
Contains functions to load data from online sources.

DATA CLEANING NOTES:
# EPISODE_LINK (KAGGLE DATA) has 174 rows instead of 180 on wiki:
# # considers S5E18-19 as 1 big episode (Raincoats) stored as E18 but no E19.
# # Omits S6E14-15 (The Highlights of 100), which contains no new content.
    No other E14-15 stored .
# # Omits S9E21-22 (The Clip Show)--contains no new content. No E21-22 stored.
# # Considers S9E23-24 (The Finale) as 1 big episode stored as E23 & no E24.

# IMDB has 173 rows:
# # Considers S3Ep17-18 (The Boyfriend) as 1 episode. Numbering after differs.
# # Considers S4Ep23-24 (The Pilot) as 1 episode. Numbering after differs.
# # DOES consider S5E18-19 as 1 big episode #18 (Raincoats).
    but also puts extra entry for #19 that can can remove!
# # DOES NOT omit S6E14-15 (The Highlights of 100). Instead stores as Ep 14.
    Numbering after differs.
# # Considers S7E14-15 as 1 big episode (The Cadillac) as E14.
    Numbering after differs.
# # Considers S7E21-22 as 1 big episode (The Bottle Deposit) as E20.
    Numbering after differs.
# # DOES NOT omits S9E21-22 (The Clip Show). Instead stores as E21.
    Numbering after differs
# # DOES consider S9E23-24 (The Finale) as 1 big episode but stores as E22.

## FYI: Netflix follows IMDb numbering (after deleting 5.19) but also
    combines S4E3-4 into 1 episode.
"""
import sys
import pandas as pd

from . import data_constants
# change to import data_constants if running this file.


def read_scripts():
    """
    Read in `Seinfeld Chronicles` script data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    df = pd.read_csv(data_constants.SCRIPTS_LINK)
    # pylint: disable=no-member
    df.drop(columns=df.columns[0], inplace=True)
    # pylint: disable=no-member
    df = df.astype({
        'Season': int,
        'EpisodeNo': int
    })
    # Fix Season 1. Ep1 is combination of Ep1&2. Need to split into 2.
    # Episode 1 ends at Line 210.
    # Map Ep1 to 0, then add 1 to all episodes in season 1.
    df.loc[0:210, 'EpisodeNo'] = 0
    season_mask = df.Season == 1
    df.loc[season_mask, 'EpisodeNo'] = df.loc[season_mask, 'EpisodeNo'] + 1
    df.loc[season_mask, 'SEID'] = df.loc[season_mask, 'SEID'].str[:4] + \
        df.loc[season_mask, 'EpisodeNo'].astype(str).str.pad(2, fillchar='0')

    # Clean Character and Dialogue Fields
    cleaned_df = _clean_scripts(df)
    return cleaned_df


def read_episode_info():
    """
    Read in `Seinfeld Chronicles` episode data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    df = pd.read_csv(data_constants.EPISODE_LINK)
    # pylint: disable=no-member
    df.drop(columns=df.columns[0], inplace=True)
    # pylint: disable=no-member
    df = df.astype({
        'Season': int,
        'EpisodeNo': int
    })
    # Fix Season 1's Mapping (have 2 Ep 1s)
    # Remap from 1,1,2,3,4 into 1,2,3,4,5
    season_mask = df.Season == 1
    for ind in df.loc[season_mask].index:
        df.loc[ind, 'EpisodeNo'] = ind + 1
        df.loc[ind, 'SEID'] = f'S01E{ind + 1:02d}'
    return df


def read_imdb_metadata():
    """
    Read in `Seinfeld Chronicles` episode data from Kaggle
    as a Data Frame.

    :return: Pandas Data Frame
    """
    seinfeld_id = data_constants.SEINFELD_PARENT_TCONST

    # Gather all episode metadata
    print('\t Gathering Episode Info...')
    all_eps = pd.read_csv(data_constants.IMDB_EPISODE, delimiter='\t')
    all_eps = all_eps[all_eps.parentTconst == seinfeld_id]
    #   Season 5, Episode 19 doubled in data.
    epi_ids = set(all_eps['tconst'].values) - {'tt19390512'}
    # Gather all rating data
    print('\t Gathering Rating Data...')
    ratings = pd.read_csv(data_constants.IMDB_RATING, delimiter='\t')
    ratings = ratings[ratings.tconst.isin(epi_ids)]
    # Gather additional metadata
    print('\t Gathering Title & Run Time Information...')
    basics = pd.read_csv(data_constants.IMDB_BASICS, delimiter='\t',
        usecols=['tconst', 'originalTitle', 'runtimeMinutes']
    )
    basics = basics[basics.tconst.isin(epi_ids)]
    # Gather all episode summary and keyword data
    print('\t Gathering Episode Descriptions, Summaries, and Keywords...')
    summaries = pd.read_csv(data_constants.IMDB_SUMMARIES)
    # Join subsets together & convert missing values to None
    final_df = (all_eps.merge(ratings, on=['tconst'])
        .merge(basics, on=['tconst'])
        .merge(summaries, on=['tconst'])
        .replace('\\N', None)
    )
    final_df = final_df.astype({
        'seasonNumber': int,
        'episodeNumber': int,
        'runtimeMinutes': float,
    })
    final_df = (final_df.sort_values(by=['seasonNumber', 'episodeNumber'])
        .reset_index(drop=True)
    )
    # Correct episode number so it matches that of Kaggle/Wiki
    map_wiki = data_constants.MAP_IMDB_WIKI
    map_netflix = data_constants.MAP_IMDB_NETFLIX
    final_df['EpisodeNo'] = (final_df[['seasonNumber', 'episodeNumber']]
        .apply(lambda x: map_wiki[x[0]].get(x[1], x[1]), axis=1)
    )
    final_df['EpiNo_Netflix'] = (final_df[['seasonNumber', 'episodeNumber']]
        .apply(lambda x: map_netflix[x[0]].get(x[1], x[1]), axis=1)
    )
    # Remove other redundant columns & clean up order
    final_df.drop(columns=['episodeNumber', 'parentTconst'], inplace=True)
    final_df.rename(columns={'seasonNumber': 'Season'}, inplace=True)

    final_df = final_df[
        ['tconst', 'originalTitle', 'Season', 'EpisodeNo', 'EpiNo_Netflix',
         'runtimeMinutes', 'numVotes', 'averageRating',
         'Description', 'Summaries', 'keyWords']]
    final_df = final_df.astype({
        'EpiNo_Netflix': int,
        'runtimeMinutes': float}
    )
    return final_df


def get_final_data(merge=False):
    """
    Collect all data sets using the above helper functions.

    :param merge: boolean, whether or not to merge all data.
    :return: 2 Dataframes (1 Metadata, 1 scripts)
            or 1 if merge==True
    """
    # The following episodes are the second part of a 2-part episode
    # that is merged for the IMDb data so they must be removed.
    kaggle_episodes_to_remove = ['S03E18', 'S04E24', 'S07E15', 'S07E22']
    # Get Kaggle Script Data
    print('Gathering Script Data...')
    scripts = read_scripts()
    # Get Kaggle Data Metadata
    print('Gathering Kaggle Metadata...')
    ep_info = read_episode_info()
    # Get IMDb Data:
    print('Gathering IMDb Data...')
    imdb_df = read_imdb_metadata()

    # Remove 2nd of 2-part episodes to match IMDb
    for epi in kaggle_episodes_to_remove:
        ep_number = int(epi[4:])
        prev_ep = epi[:4] + f'{ep_number - 1:02d}'
        # pylint: disable=no-member
        scripts.loc[scripts.SEID == epi, 'SEID'] = prev_ep

    ep_info = ep_info[
        ~ep_info.SEID.isin(kaggle_episodes_to_remove)]

    # Merge Data Together
    merged_df = ep_info.merge(imdb_df,
        on=['Season', 'EpisodeNo'], how='left')
    merged_df.drop(columns=['Title'], inplace=True)
    merged_df.rename(columns={'originalTitle': 'Title'}, inplace=True)

    # Fix Typo in Director's Name
    merged_df.loc[merged_df.SEID=="S03E08", "Director"] = "David Steinberg"

    scripts.drop(columns=['EpisodeNo'], inplace=True)
    scripts['EpisodeNo'] = scripts.SEID.str[4:].astype(int)

    if merge:
        merged_df.drop(columns=['Season', 'EpisodeNo'], inplace=True)
        # pylint: disable=no-member
        all_merged = scripts.merge(merged_df, on='SEID', how='left')
        return all_merged

    return merged_df, scripts


def _clean_scripts(data):
    """
    A weakly private wrapper function that cleans `Character` and
    `Dialogue` for the script data from Kaggle that will only be called
    by `read_scripts()`.
    Calls functions _drop_unneccesary_ rows

    :param data: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID'
                 MUST have unchanged row indices from original source.

    :return: Pandas DataFrame with cleaned 'Character' and 'Dialogue'.
    """
    data = __drop_poor_dialogue(data)
    data = __merge_character_dialogue(data)
    data = __fix_alias_mapping(data)
    return data


def __drop_poor_dialogue(data):
    """
    A strongly private function that removes unnecessary lines of
    dialogue from the script data.

    :param data: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID'
                 MUST have unchanged row indices from original source.
    :return: Pandas DataFrame
    """
    # rows that have '(** Footnote' or `(*` using regex:
    drop_index = data[data.Character.str.match(r'\(\*')].index
    data.drop(index=drop_index, inplace=True)
    # rows that have '(IMG SRC=http' using regex:
    drop_index = data[data.Character.str.contains(r'IMG')].index
    data.drop(index=drop_index, inplace=True)
    # rows that have http
    drop_index = data[data.Character.str.contains(r'http')].index
    data.drop(index=drop_index, inplace=True)
    # rows that have * in the character name using regex:
    drop_index = data[data.Character.str.match(r'\*')].index
    data.drop(index=drop_index, inplace=True)
    # rows that have sari/saree using regex:
    drop_index = data[data.Character.str.contains(r'Sari')].index
    data.drop(index=drop_index, inplace=True)
    # rows that have NOTE using regex:
    drop_index = data[data.Character.str.contains(r'NOTE')].index
    data.drop(index=drop_index, inplace=True)
    # definitions of chicken:
    drop_index = data[data.Character.str.contains(r'Definitions')].index
    data.drop(index=drop_index, inplace=True)
    # arbitrary citations at the end of S03E01:
    data.drop(index=[4717, 4718, 4719], inplace=True)
    # dedication at the end of S09E16:
    data.drop(index=52622, inplace=True)
    # definitions of berries
    data.drop(index=[13530, 13531], inplace=True)
    # Useless description in S04E23
    #       (Char: '(Jerry and TV Elaine' Dialog: 'Sandi Robbins)'
    data.drop(index=18151, inplace=True)

    return data


# pylint: disable=too-many-statements
def __merge_character_dialogue(data):
    """
    A strongly private function that handles cases when part of the
    dialogue is in the character column for the script data.

    :param data: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID'
                 MUST have unchanged row indices from original source.
    :return: Pandas DataFrame
    """
    # SETTING encased in [] split between character and dialogue.
    #   easy matches with str.match(r'\[.*')
    #   if the dialogue is null, fill in ]
    miss_index = data[
        data.Character.str.match(r'\[.*') & data.Dialogue.isna()].index
    data.loc[miss_index, 'Dialogue'] = ']'
    merge_index = data[data.Character.str.match(r'\[.*')].index
    data.loc[merge_index, 'Dialogue'] = data.loc[merge_index, 'Character'] + \
        ' ' + data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = 'SETTING'

    # WEIRD MERGE SCENARIOS
    # Char: (Alison though phone)
    #     replace with ALISON, and add (through phone) to dialogue
    merge_index = data[data.Character.str.match(r'\(Alison')].index
    data.loc[merge_index, 'Dialogue'] = '(Through phone) ' + \
        data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = 'ALISON'
    # Char: ""(At the same time--DONNA"
    #     Dialogue: "Hello...--ELAINE Hi! How are you?)
    merge_index = data[data.Character.str.match(r'\(At the same')].index
    data.loc[merge_index, 'Dialogue'] = '(At the same time) Hello... ' \
                                        'Hi! How are you?'
    data.loc[merge_index, 'Character'] = 'DONNA & ELAINE'
    # Char: (Everyone sits around the table. Kruger recognized
    #     Kramer from "The Meat Slicer" episode..) KRUGER
    #     Make into Char: KRUGER, Dialogue = (action) Dr. Van Nostrand?
    merge_index = data[
        data.Character.str.match(r'\(Everyone sits around')].index
    data.loc[merge_index, 'Dialogue'] = '(Everyone sits around the table. ' \
                                        'Kruger recognized Kramer from ' \
                                        '"The Meat Slicer" episode.) ' \
                                        'Dr. Van Nostrand?'
    data.loc[merge_index, 'Character'] = 'KRUGER'
    # Weird Things in S04E23 dealing with the show inside the show
    #     18353-18356 drop
    data.loc[18353, 'Dialogue'] = "[(TV Show Runs..) We see the title " \
                                  "'Jerry', then, sitting at the comedy" \
                                  " club, we see Micheal, Sandi, and " \
                                  "Tom, and finally Jerry, and the four" \
                                  " of them make a toast while it's " \
                                  "written 'Created by Jerry Seinfeld " \
                                  "and George Costanza']"
    data.loc[18353, 'Character'] = 'SETTING'
    data.drop(index=[18354, 18355, 18356], inplace=True)
    # Lines from a movie that the four attend
    #     loc [35255, 35260,35274]
    data.loc[35255, 'Dialogue'] = data.loc[35255, 'Dialogue'].split(' --')[0]
    data.loc[[35255, 35260, 35274], 'Character'] = 'MOVIE'
    #     loc 41490
    data.loc[41490, 'Dialogue'] = data.loc[41490, 'Dialogue'].split(')')[0]
    data.loc[41490, 'Character'] = 'MOVIE'
    # Missing closing parenthesis 34896
    data.loc[34896, 'Dialogue'] = data.loc[34896, 'Character'] + ' ' + \
                                  data.loc[34896, 'Dialogue'] + ')'
    data.loc[34896, 'Character'] = 'SETTING'

    # MORE WEIRD SCENARIOS
    # .loc 43600 Char: Check #1246, dated Dec. 15 96, Made out to
    data.loc[43600, 'Dialogue'] = 'Check #1246, dated Dec. 15, 1996, ' \
                                  'Made out to ' + \
                                  data.loc[43600, 'Dialogue']
    data.loc[43600, 'Character'] = 'SETTING'
    # .loc 4715 Char: Song over the end credits
    data.loc[4715, 'Dialogue'] = '(Song over the end credits) ' + \
                                 data.loc[4715, 'Dialogue']
    data.loc[4715, 'Character'] = 'SETTING'
    # .loc 34212 Char: We gotta go! It's 8
    data.loc[34212, 'Dialogue'] = "We gotta go! It's 8" + \
                                  data.loc[34212, 'Dialogue']
    data.loc[34212, 'Character'] = 'JERRY'
    # .loc 50044 Char: Elaine, becoming board
    data.loc[50044, 'Dialogue'] = "(Becoming bored) " + \
                                  data.loc[50044, 'Dialogue']
    data.loc[50044, 'Character'] = 'ELAINE'
    # .loc 47952 Char: Scene
    data.loc[47952, 'Dialogue'] = '[Scene ' + data.loc[47952, 'Dialogue']
    data.loc[47952, 'Character'] = 'SETTING'
    # .loc 10902 Char: Opening scene
    data.loc[10902, 'Dialogue'] = '[Scene ' + data.loc[10902, 'Dialogue']
    data.loc[10902, 'Character'] = 'SETTING'

    # SETTING encased in () split between character and dialogue.
    #     str.match(r'\(.*')
    merge_index = data[data.Character.str.match(r'\(.*')].index
    data.loc[merge_index, 'Dialogue'] = data.loc[merge_index, 'Character'] + \
        ' ' + data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = 'SETTING'

    # SETTING indicated by % in S04E14
    merge_index = data[data.Character.str.match(r'%')].index
    data.loc[merge_index, 'Dialogue'] = data.loc[
        merge_index, 'Character'].str.split('% ', expand=True)[1] + \
        ' ' + data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = 'SETTING'

    # Jerry's monologue gets split up
    char_len = data.Character.apply(lambda x: len(x.split()))
    merge_index = data[char_len > 16].index
    data.loc[merge_index, 'Dialogue'] = data.loc[merge_index, 'Character'] + \
        ' ' + data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = 'JERRY'

    # Char: 'Notice' in S09E08
    #     missing value for loc 49651
    data.loc[49651, 'Dialogue'] = '"FOUR HOURS EARLIER, BACK IN NEW YORK"'
    merge_index = data[data.Character.str.match('Notice')].index
    data.loc[merge_index, 'Dialogue'] = data.loc[merge_index, 'Character'] + \
        ': ' + data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = 'SETTING'

    # Char: MONTAGE in S09E18
    fix_index = data[data.Character.str.contains(r"MONTAGE")].index
    data.loc[fix_index, 'Character'] = 'SETTING'
    data.loc[fix_index, 'Dialogue'] = '[Montage of Jerry and Lisi ' \
                                      'arguing/breaking up.]'

    # Parenthesis in Character column along with character name:
    #       sometimes it is is an alias name,
    #       other times its descriptions.
    # Check with data[data.Character.str.contains('\([A-Z]+\)')]
    # Fix Cases of aliases in brackets
    fix_index = data[data.Character.str.contains('RESTAURANT MANAGER')].index
    data.loc[fix_index, 'Character'] = "BRUCE"
    # If character is `char A & char B`, leave as is,
    #       later attribute the line to both chars
    # If character is `char A (some action)`, change to `char A`
    #       and put `(some action)` at the beginning of dialogue
    merge_index = data[data.Character.str.contains(r'\(.+\)')].index
    data.loc[merge_index, 'Dialogue'] = '(' + data.loc[
        merge_index, 'Character'].str.split(r'\(', expand=True)[1] + \
        ' ' + data.loc[merge_index, 'Dialogue']
    data.loc[merge_index, 'Character'] = data.loc[
        merge_index, 'Character'].str.split(r'\(', expand=True)[0]

    return data


# pylint: disable=too-many-statements
def __fix_alias_mapping(data):
    """
    A strongly private function that handles mapping of aliases for
    character names as well as cases for missing values of dialogues
    for the script data.

    :param data: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID'
                 MUST have unchanged row indices from original source.
    :return: Pandas DataFrame
    """
    # Missing dialogue for Hal in S08E18: loc 45847
    data.loc[45847, 'Dialogue'] = "You know Twinkies aren't cooked?"

    # Character Fixes:
    # .loc 10901 Char: Jerry's stand-up
    data.loc[10901, 'Character'] = 'JERRY'
    # .loc 5621 Char: JERRY and ELAINE, together
    data.loc[5621, 'Character'] = 'JERRY & ELAINE'
    # .loc 23385 Char: Opening Monolog
    data.loc[23385, 'Character'] = 'JERRY'
    # .loc 39522 Char: so far
    data.loc[39522, 'Character'] = 'SETTING'
    # .loc 36528 Char: JERRY\x92S OUTGOING MESSAGE
    data.loc[36528, 'Character'] = "JERRY's ANSWERING MACHINE"
    # .loc 1461 Char: JERRY\x92S MESSAGE
    data.loc[1461, 'Character'] = "JERRY's ANSWERING MACHINE"

    # Convert {',', 'AND', 'and', '+', '/'} to '&'
    #     ', &'-> ' &'
    fix_index = data[data.Character.str.contains(', &')].index
    data.loc[fix_index, 'Character'] = data.loc[
        fix_index, 'Character'].str.replace(', &', ' &')
    #     ', ' -> ' &'
    fix_index = data[data.Character.str.contains(', ')].index
    data.loc[fix_index, 'Character'] = data.loc[
        fix_index, 'Character'].str.replace(', ', ' & ')
    #     '+' -> '&'
    fix_index = data[data.Character.str.contains(r'\+')].index
    data.loc[fix_index, 'Character'] = data.loc[
        fix_index, 'Character'].str.replace('+', '&', regex=False)
    #     ' and ' -> ' & '
    fix_index = data[data.Character.str.contains(' and ')].index
    data.loc[fix_index, 'Character'] = data.loc[
        fix_index, 'Character'].str.replace(' and ', ' & ')
    #     ' AND ' -> ' & '
    fix_index = data[data.Character.str.contains(' AND ')].index
    data.loc[fix_index, 'Character'] = data.loc[
        fix_index, 'Character'].str.replace(' AND ', ' & ')
    #     'word&word' -> 'word & word'
    fix_index = data[data.Character.str.match('^[A-Z]+&[A-Z]+$')].index
    data.loc[fix_index, 'Character'] = (data.loc[fix_index].Character.str
                                        .extract('^([A-Z]+)&([A-Z]+)$')
                                        ).agg(' & '.join, axis=1)
    #     'word/word' -> 'word & word'
    fix_index = data[data.Character.str.contains('/')].index
    data.loc[fix_index, 'Character'] = (data.loc[fix_index, 'Character']
                                        .str.replace('/', ' & '))

    # Remove White Space
    data.Character = data.Character.str.strip()

    # Replace \x92 with '
    data.Character = data.Character.str.replace(r'[\x92]', "'", regex=True)
    data.Dialogue = data.Dialogue.str.replace(r'[\x92]', "'", regex=True)

    # MAPPING ALIASES:
    #     Hx, JERR, JERY -> JERRY
    data.loc[data.Character.isin(['Hx', 'JERR', 'JERY']),
             'Character'] = 'JERRY'
    #     Ex, ELANE, ELAIEN, ELIANE, EALINE, ElainELAINE -> ELAINE
    data.loc[data.Character.isin(
        ['Ex', 'ELANE', 'ELAIEN', 'ELIANE', 'EALINE', 'ElainELAINE']),
             'Character'] = 'ELAINE'
    #     GX, GEOGE, GEROGE, GOERGE -> GEORGE
    data.loc[data.Character.isin(['GX', 'GEOGE', 'GOERGE', 'GEROGE']),
             'Character'] = 'GEORGE'
    #     NEWMANEWMAN, NEMWAN -> NEWMAN
    data.loc[data.Character.isin(['NEWMANEWMAN', 'NEMWAN']),
             'Character'] = 'NEWMAN'
    #     KRMAER -> KRAMER
    data.loc[data.Character.isin(['KRMAER']), 'Character'] = 'KRAMER'
    #     MRS. COSTANZA, MRS. C -> ESTELLE
    data.loc[data.Character.isin(['MRS. COSTANZA', 'MRS. C']),
             'Character'] = 'ESTELLE'
    #     MRS. S > HELEN (SEINFELD)
    data.loc[data.Character.isin(['MRS. S']), 'Character'] = 'HELEN'
    #     MR. S > MORTY (SEINFELD)
    data.loc[data.Character.isin(['MR. S']), 'Character'] = 'MORTY'
    #     Dx -> DOCTOR
    data.loc[data.Character.isin(['Dx']), 'Character'] = 'DOCTOR'
    #     Wx -> WAITRESS
    data.loc[data.Character.isin(['Wx']), 'Character'] = 'WAITRESS'
    #     Babu Bhatt -> BABU
    data.loc[data.Character.isin(['Babu Bhatt']), 'Character'] = 'BABU'
    #     EDDIT -> EDDIE
    data.loc[data.Character.isin(['EDDIT']), 'Character'] = 'EDDIE'
    #     GUAD, GAURD -> GUARD
    data.loc[data.Character.isin(['GUAD', 'GAURD']), 'Character'] = 'GUARD'
    #     MR.THOMASSOULO,MR. THOMASSOULO -> THOMASSOULO
    data.loc[data.Character.isin(['MR.THOMASSOULO', 'MR. THOMASSOULO']),
             'Character'] = 'THOMASSOULO'
    #     'MR. PETERMAN', J. PETERMAN -> PETERMAN
    data.loc[data.Character.isin(['MR. PETERMAN', 'J. PETERMAN']),
             'Character'] = 'PETERMAN'
    #     'MR. PITT' -> PITT
    data.loc[data.Character.isin(['MR. PITT']), 'Character'] = 'PITT'
    #     'MR. LIPPMAN' -> LIPPMAN
    data.loc[data.Character.isin(['MR. LIPPMAN']), 'Character'] = 'LIPPMAN'
    #     MR ROSS -> 'MR. ROSS'
    data.loc[data.Character.isin(['MR ROSS']), 'Character'] = 'MR. ROSS'
    #     'MR. STEINBRENNER' -> STEINBRENNER
    data.loc[data.Character.isin(['MR. STEINBRENNER']),
             'Character'] = 'STEINBRENNER'
    #     TVVOICE, TV VOICE, TV ANNOUNCER, TV NEWSCASTER -> TV
    data.loc[data.Character.isin(
        ['TVVOICE', 'TV VOICE', 'TV ANNOUNCER',
         'TV NEWSCASTER', 'ANNOUNCER ON TV']), 'Character'] = 'TV'
    #     WOMANEWMAN -> WOMAN
    data.loc[data.Character.isin(['WOMANEWMAN']), 'Character'] = 'WOMAN'
    #     MORGANEWMAN, MORGAN-> MR. MORGAN
    data.loc[data.Character.isin(['MORGANEWMAN', 'MORGAN']),
             'Character'] = 'MR. MORGAN'
    #     C.K -> CALVIN KLEIN
    data.loc[data.Character.isin(['C.K.']), 'Character'] = 'CALVIN KLEIN'
    #     # SeConrad -> SECRETARY
    data.loc[data.Character.isin(['SeConrad']),'Character'] = 'SECRETARY'
    #     "SALMAN" -> SAL BASS
    data.loc[data.Character.isin(['"SALMAN"']), 'Character'] = 'SAL BASS'
    #    ANSWERING MACHINE, JERRY'S MACHINE, MACHINE
    #       -> JERRY'S ANSWERING MACHINE
    data.loc[data.Character.isin(
        ["ANSWERING MACHINE", "JERRY'S MACHINE", 'MACHINE']),
             'Character'] = "JERRY'S ANSWERING MACHINE"
    # 'IZZY IZZY SR..' -> 'IZZY SR.'
    data.loc[data.Character.isin(['IZZY IZZY SR..']),
             'Character'] = 'IZZY SR.'
    # 'IZZY & IZZY JR & IZZY IZZY SR. -> IZZY & IZZY JR. & IZZY SR.
    data.loc[data.Character.isin(['IZZY & IZZY JR & IZZY IZZY SR.']),
             'Character'] = 'IZZY & IZZY JR. & IZZY SR.'
    #     CLAIE -> CLAIRE (WAITRESS)
    data.loc[data.Character.isin(['CLAIE']), 'Character'] = 'CLAIRE'

    # Check that all characters are capitalized
    data.Character = data.Character.str.upper()

    #     BENES, ALTON -> ALTON BENES (ELAINE's Dad)
    data.loc[data.Character.isin(['BENES', 'ALTON']),
             'Character'] = 'ALTON BENES'
    #     MARRY, MAR -> MARY
    data.loc[data.Character.isin(['MARRY', 'MAR']), 'Character'] = 'MARY'
    #     SPONSER, SPONER -> SPONSOR
    data.loc[data.Character.isin(['SPONSER', 'SPONER']),
             'Character'] = 'SPONSOR'
    #     SLIPPERT PETE -> SPLIPPERY PETE
    data.loc[data.Character.isin(['SLIPPERT PETE']),
             'Character'] = 'SLIPPERY PETE'
    #     DRY CLEANE -> DRY CLEANER
    data.loc[data.Character.isin(['DRY CLEANE']),
             'Character'] = 'DRY CLEANER'
    #     AENT -> AGENT
    data.loc[data.Character.isin(['AENT']),
             'Character'] = 'AGENT'
    # standardize CHAR's mind, CHAR's VOICE, thinking, etc.
    #     check with data[data.Character.str.contains("'S")]
    #     ELAINE
    fix_index = data[data.Character.isin(
        ["ELAINE THINKING", "ELAINE'S VOICE", "ELAINE'S BRAIN"])].index
    data.loc[fix_index, 'Character'] = "ELAINE"
    data.loc[fix_index, 'Dialogue'] = "(MIND) " + \
                                      data.loc[fix_index, 'Dialogue']
    #     GEORGE
    fix_index = data[data.Character.isin(["GEORGE'S VOICE"])].index
    data.loc[fix_index, 'Character'] = "GEORGE"
    data.loc[fix_index, 'Dialogue'] = "(MIND) " + \
                                      data.loc[fix_index, 'Dialogue']
    #     JERRY'S BRAIN is mental dialogue
    #           but is a character in S03E09
    fix_index = data[data.Character.isin(["JERRY'S BRAIN"])
                     & (data.SEID != 'S03E09')].index
    data.loc[fix_index, 'Character'] = "JERRY"
    data.loc[fix_index, 'Dialogue'] = "(MIND) " + \
                                      data.loc[fix_index, 'Dialogue']

    # Remove . and #
    data.Character = data.Character.str.replace('.', '', regex=False)
    data.Character = data.Character.str.replace('#', '', regex=False)

    # Remove White Space
    data.Character = data.Character.str.strip()

    return data


if __name__ == '__main__':
    cwd = sys.argv[1]
    base_path = cwd.split("an_analysis_of_nothing", maxsplit=1)[0]
    data_folder = base_path + 'an_analysis_of_nothing/data/'
    meta_name = data_folder + 'metadata.csv'
    script_name = data_folder + 'scripts.csv'
    meta, scripts = get_final_data()
    meta.to_csv(meta_name, index=False)
    scripts.to_csv(script_name, index=False)
