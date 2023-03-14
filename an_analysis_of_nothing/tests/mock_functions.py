"""
    Module for mock function calls.
"""
import pandas as pd
from utils import data_constants


def mocked_read_csv(*args):
    """
        This is a mock function for loading data.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
         "Art Wolff", "S01E01", "tt0098286",
         "Good News, Bad News", 1, 23, "6031", 7.4, "Jerry and George argue \
        whether an overnight visitor \
        Jerry is expecting is coming with romantic intentions. ", """["In \
        this episode, the predecessor to Seinfeld \
        (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York.\
        Throughout the first part of the show Jerry and \
        George are discussing the situation. Later we meet 'Kessler' \
        who comes in to Jerry\'s apartment to borrow some \
        meat and uncharacteristically \
        knocks on the door before entering."]""", "['tv series pilot', \
        'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport',\
        'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', \
        'laundromat', 'romantic interest', 'realtor', 'overnight', \
        'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', \
        'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer',\
        'refrigerator', \
        'sandwich', 'sitting on a couch', 'eating cereal', \
        'cereal', 'magazine', 'waiting', 'surprise', 'handshake', \
        'luggage', 'help', 'relaxation', 'hospitality', 'lap', \
        'man takes off shoes', \
        'wine bottle', 'red wine', 'evening', 'audience', \
        'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 7.5, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],
    ]
    data_scripts_raw = [
        ['JERRY', 'Do you know what this is all about? \
        Do you know, why were here? To be out, \
        this is out...and out is one of the single most enjoyable experiences of life. People...\
        did you ever hear people talking about We should go out? This is what theyre talking about...\
        this whole thing, were all out now, no one is home. Not one person here is home, were all out! \
        There are people tryin to find us, they dont know where we are. (on an imaginary phone) Did you ring?, \
        I cant find him. Where did he go? He didnt tell me where he was going. \
        He must have gone out. You wanna go out you get ready, you pick out the clothes, right? You take \
        the shower, you get all ready, get the cash, get your friends, the car, the spot, the reservation..\
        .Then youre standing around, whatta you do? You go We gotta be getting back. Once youre out, \
        you wanna get back! You wanna go to sleep, you wanna get up, you wanna go out again tomorrow, right? \
        Where ever you are in life, its my feeling, youve gotta go.', 'S01E01',
         1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
        ['JERRY', '(pointing at Georges shirt) See, to me, that button is in \
        the worst possible spot. \
        The second button literally makes or breaks the shirt, look at it.\
        Its too high! Its in no-mans-land. \
        You look like you live with your mother.',
         'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['JERRY', 'You do of course try on, when you buy?',
            'S01E01', 1, 1, 0, 0, 0, 0, 0, 9],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
    ]

    mock_imdb_data = pd.DataFrame(
        data_imdb_raw, columns=['Season', 'EpisodeNo', 'AirDate',
                                'Writers', 'Director', 'SEID', 'tconst',
                                'Title', 'EpiNo_Netflix',
                                'runtimeMinutes', 'numVotes', 'averageRating',
                                'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data


def mocked_read_csv_duplicate(*args):
    """
    This is a mock function for loading data.
    This contains episodes with the same summary.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
            "Art Wolff", "S01E01", "tt0098286", "Good News, Bad News",
            1, 23, "6031", 7.4, "Jerry and George argue whether an overnight \
            visitor Jerry is expecting is coming with romantic intentions. ",
            """["In this episode, the predecessor to \
                Seinfeld (1989), Jerry is \
                expecting a woman that he met in Michigan \
                    to come and visit him in New York. \
                Throughout the first part of the show \
                    Jerry and George are discussing the \
                situation. Later we meet 'Kessler' \
                    who comes in to Jerry\'s apartment to \
                borrow some meat and uncharacteristically \
                    knocks on the door before entering."]""",
         "['tv series pilot', 'cafe', 'waitress', 'coffee', 'friend', \
                'apartment', 'airport', \
                'greeting', 'wine', 'dog', 'bread', \
                    'meat', 'mattress', 'laundromat']"],
        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02",
         "tt0697784", "The Stakeout", 2, 23, "5113",
         7.5, "Jerry and George stake \
            out the lobby of an office building to find \
                a woman Jerry met at a party but\
            whose name and phone number he didn't get.",
            """["Elaine drags Jerry to a \
            birthday dinner for one of her friends where \
                he meets an attractive woman. \
            He promptly forgets her name and refuses to \
            ask Elaine who she is but remembers \
            where she works. Jerry's parents are in town \
            to go to a family wedding and his Dad \
            suggests he stake-out the lobby around lunchtime. \
             George tags along but they can't quite\
            seem to get their stories straight. \
                Elaine hears about it making them both \
            uncomfortable."]""",
            """['reference to loni anderson', 'pornography',
            'fake name', 'scrabble', 'hearing characters thoughts',
            'made up word', 'reference to john cougar mellencamp',
            'reference to ethel merman',
            'polishing shoes', 'birthday party', 'dream', 'video store']"""],
        [1, 3, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E03",
         "tt0697784", "The Stakeout2", 2, 23, "5113",
         7.5, "Jerry and George stake \
            out the lobby of an office building to find a woman Jerry met at a party but\
            whose name and phone number he didn't get.",
         """["Elaine drags Jerry to a \
            birthday dinner for one of her friends \
                where he meets an attractive woman. \
            He promptly forgets her name and refuses to \
                ask Elaine who she is but remembers \
            where she works. Jerry's parents are in town \
                to go to a family wedding and his Dad \
            suggests he stake-out the lobby around lunchtime. \
                George tags along but they can't quite\
            seem to get their stories straight. \
                Elaine hears about it making them both \
            uncomfortable."]""",
            """['reference to loni anderson', 'pornography',
            'fake name', 'scrabble', 'hearing characters thoughts',
            'made up word', 'reference to john cougar mellencamp',
            'reference to ethel merman',
            'polishing shoes', 'birthday party', 'dream', 'video store']"""],
        [1, 4, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E04",
         "tt0697784", "The Stakeout3", 2, 23,
         "5113", 7.5, "Jerry and George stake \
        out the lobby of an office building to find a woman Jerry met at a party but\
        whose name and phone number he didn't get.",
         """["Elaine drags Jerry to a \
        birthday dinner for one of her friends where he meets \
        an attractive woman. \
        He promptly forgets her name and refuses to ask \
        Elaine who she is but remembers \
        where she works. Jerry's parents are in town to go \
        to a family wedding and his Dad \
        suggests he stake-out the lobby around lunchtime. \
        George tags along but they can't quite\
        seem to get their stories straight. Elaine hears \
        about it making them both \
        uncomfortable."]""",
         """['reference to loni anderson', 'pornography',
        'fake name', 'scrabble', 'hearing characters thoughts',
        'made up word', 'reference to john cougar mellencamp',
        'reference to ethel merman',
        'polishing shoes', 'birthday party', 'dream', 'video store']"""],
    ]
    data_scripts_raw = [
        ['JERRY', 'Do you know what this is all about? Do you know, \
            why were here? To be out, this is out...and out is one of \
            the single most enjoyable experiences of life. People...\
            did you ever hear people talking about We should go out? \
            This is what theyre talking about...this whole thing, were \
            all out now, no one is home. Not one person here is home, \
            were all out! There are people tryin to find us, they \
            dont know where we are. (on an imaginary phone)\
            Did you ring?, I cant find him. Where did he go?',
            'S01E01', 1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
        ['JERRY', '(pointing at Georges shirt) See, to me, that button \
            is in the worst possible spot. The second button literally makes \
            or breaks the shirt, look at it. Its too high! Its in \
            no-mans-land. You look like you live with your mother.', 'S01E01',
            1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['JERRY', 'You do of course try on, when you buy?',
            'S01E01', 1, 1, 0, 0, 0, 0, 0, 9],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually \
            recall considering the buttons.',
            'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
        ['MAN', 'Yes, it was purple, I liked it, I dont actually recall \
            considering the buttons.', 'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
        ['WOMAN', 'Yes, it was purple, I liked it, I dont actually \
            recall considering the buttons.',
            'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
        ['SETTING', 'Yes, it was purple, I liked it, I dont actually \
            recall considering the buttons.',
            'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually \
            recall considering the buttons.',
            'S01E03', 1, 3, 0, 0.5, 0, 0.5, 0, 14],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually \
            recall considering the buttons.',
            'S01E04', 1, 4, 0, 0.5, 0, 0.5, 0, 14]

    ]*110

    mock_imdb_data = pd.DataFrame(data_imdb_raw,
                                  columns=['Season', 'EpisodeNo',
                                           'AirDate', 'Writers',
                                           'Director', 'SEID',
                                           'tconst', 'Title',
                                           'EpiNo_Netflix', 'runtimeMinutes',
                                           'numVotes', 'averageRating',
                                           'Description', 'Summaries',
                                           'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw,
                                    columns=['Character',
                                             'Dialogue', 'SEID',
                                             'Season', 'EpisodeNo',
                                             'Happy', 'Angry', 'Surprise',
                                             'Sad', 'Fear', 'numWords'])
    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data


def mocked_character_read_csv(*args):
    """
    Mocked data with random new character added.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
         "Art Wolff", "S01E01", "tt0098286",
         "Good News, Bad News", 1, 23, "6031", 7.4, "Jerry and George argue \
        whether an overnight visitor \
        Jerry is expecting is coming with romantic intentions. ", """["In \
        this episode, the predecessor to Seinfeld \
        (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York.\
        Throughout the first part of the show Jerry and \
        George are discussing the situation. Later we meet 'Kessler' \
        who comes in to Jerry\'s apartment to borrow some \
        meat and uncharacteristically \
        knocks on the door before entering."]""", "['tv series pilot', \
        'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport',\
        'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', \
        'laundromat', 'romantic interest', 'realtor', 'overnight', \
        'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', \
        'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer',\
        'refrigerator', \
        'sandwich', 'sitting on a couch', 'eating cereal', \
        'cereal', 'magazine', 'waiting', 'surprise', 'handshake', \
        'luggage', 'help', 'relaxation', 'hospitality', 'lap', 'man takes off shoes', \
        'wine bottle', 'red wine', 'evening', \
        'audience', 'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 7.5, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],
    ]
    data_scripts_raw = [
        ['JERRY', 'Do you know what this is all about? \
        Do you know, why were here? To be out, \
        this is out...and out is one of the single most enjoyable experiences of life. People...\
        did you ever hear people talking about We should go out? This is what theyre talking about...\
        this whole thing, were all out now, no one is home. Not one person here is home, were all out! \
        There are people tryin to find us, they dont know where we are. (on an imaginary phone) Did you ring?, \
        I cant find him. Where did he go? He didnt tell me where he was going. \
        He must have gone out. You wanna go out you get ready, you pick out the clothes, right? You take \
        the shower, you get all ready, get the cash, get your friends, the car, the spot, the reservation..\
        .Then youre standing around, whatta you do? You go We gotta be getting back. Once youre out, \
        you wanna get back! You wanna go to sleep, you wanna get up, you wanna go out again tomorrow, right? \
        Where ever you are in life, its my feeling, youve gotta go.', 'S01E01',
         1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
        ['JERRY', '(pointing at Georges shirt) See, to me, that button is in \
        the worst possible spot. \
        The second button literally makes or breaks the shirt, look at it.\
        Its too high! Its in no-mans-land. \
        You look like you live with your mother.',
         'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['JERRY & GEORGE', 'You do of course try on, when you buy?',
            'S01E01', 1, 1, 0, 0, 0, 0, 0, 9],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 3, 0, 0.5, 0, 0.5, 0, 14],
        ['PETER', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 3, 0, 0.5, 0, 0.5, 0, 14],
    ]

    mock_imdb_data = pd.DataFrame(data_imdb_raw,
                                  columns=[
                                      'Season', 'EpisodeNo', 'AirDate',
                                      'Writers',
                                      'Director', 'SEID', 'tconst',
                                      'Title', 'EpiNo_Netflix',
                                      'runtimeMinutes',
                                      'numVotes', 'averageRating',
                                      'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data


def mocked_read_csv_large(*args):
    """
        This is a mock function for loading data.
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
         "Art Wolff", "S01E01", "tt0098286",
         "Good News, Bad News", 1, 23, "6031", 7.4, "Jerry and George argue \
        whether an overnight visitor \
        Jerry is expecting is coming with romantic intentions. ", """["In \
        this episode, the predecessor to Seinfeld \
        (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York.\
        Throughout the first part of the show Jerry and \
        George are discussing the situation. Later we meet 'Kessler' \
        who comes in to Jerry\'s apartment to borrow some \
        meat and uncharacteristically \
        knocks on the door before entering."]""", "['tv series pilot', \
        'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport',\
        'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', \
        'laundromat', 'romantic interest', 'realtor', 'overnight', \
        'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', \
        'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer',\
        'refrigerator', \
        'sandwich', 'sitting on a couch', 'eating cereal', \
        'cereal', 'magazine', 'waiting', 'surprise', 'handshake', \
        'luggage', 'help', 'relaxation', 'hospitality', 'lap', 'man takes off shoes', \
        'wine bottle', 'red wine', 'evening', 'audience',\
        'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 9, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],

        [4, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones",
         "S04E02", "tt0697784",
         "The Stakeout", 4, 23, "5113", 8, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],
    ]
    data_scripts_raw = [
        ['JERRY', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['KRAMER', 'Are you through?', 'S01E02', 1, 2, 0, 0, 0, 0, 0, 3],
        ['GEORGE', 'Are you through?', 'S04E02', 4, 2, 0, 0, 0, 0, 0, 3],
    ] * 50000

    mock_imdb_data = pd.DataFrame(
        data_imdb_raw, columns=['Season',
                                'EpisodeNo', 'AirDate', 'Writers',
                                'Director', 'SEID', 'tconst',
                                'Title', 'EpiNo_Netflix', 'runtimeMinutes',
                                'numVotes', 'averageRating',
                                'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data


def mocked_read_csv_query(*args):
    """
        This function mocks pd.read_csv and return either scripts
        or imdb dataframes.
        :return: Pandas Dataframe
    """
    data_imdb_raw = [
        [1, 1, "July 5, 1989", "Larry David, Jerry Seinfeld",
         "Art Wolff", "S01E01", "tt0098286",
         "Good News, Bad News", 1, 23, "6031", 7.4,
         "Jerry and George argue \
        whether an overnight visitor \
        Jerry is expecting is coming with romantic intentions. ", """["In \
        this episode, the predecessor to Seinfeld \
        (1989), Jerry is expecting a woman that he met in Michigan to come and visit him in New York.\
        Throughout the first part of the show Jerry and \
        George are discussing the situation. Later we meet 'Kessler' \
        who comes in to Jerry\'s apartment to borrow some \
        meat and uncharacteristically \
        knocks on the door before entering."]""", "['tv series pilot', \
        'cafe', 'waitress', 'coffee', 'friend', 'apartment', 'airport',\
        'greeting', 'wine', 'dog', 'bread', 'meat', 'mattress', \
        'laundromat', 'romantic interest', 'realtor', 'overnight', \
        'visitor', 'intentions', 'milk', 'decaf', 'purple shirt', 'button', \
        'purple', 'shirt', 'misunderstanding', 'watching tv', 'clothes dryer',\
        'refrigerator', \
        'sandwich', 'sitting on a couch', 'eating cereal', \
        'cereal', 'magazine', 'waiting', 'surprise', 'handshake', \
        'luggage', 'help', 'relaxation', 'hospitality', 'lap', 'man takes off shoes', \
        'wine bottle', 'red wine', 'evening', \
        'audience', 'watching sports on tv']"],

        [1, 2, "May 31, 1990", "Larry David, Jerry Seinfeld",
         "Tom Cherones", "S01E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 9, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],

        [2, 2, "May 31, 1990", "Larry David, Jerry Seinfeld", "Tom Cherones",
         "S02E02", "tt0697784",
         "The Stakeout", 2, 23, "5113", 1, "Jerry and George stake \
        out the lobby of an office building to \
        find a woman Jerry met at a party but whose name and phone \
        number he didn't get.",
         """["Elaine drags Jerry to a birthday dinner for one of her friends \
        where he meets an attractive woman. \
        He promptly forgets her name and refuses to ask Elaine who she is but \
        remembers where she works. Jerry's parents are \
        in town to go to a family wedding and his Dad suggests he stake-out \
        the lobby around lunchtime. George tags along \
        but they can't quite seem to get their stories straight. Elaine hears \
        about it making them both uncomfortable."]""",
         "['reference to loni anderson', 'pornography', 'fake name', \
        'scrabble', 'hearing characters thoughts', 'made up word', \
        'reference to john cougar mellencamp', 'reference to ethel merman', \
        'polishing shoes', 'birthday party', 'dream', 'video store']"],
    ]
    data_scripts_raw = [
        ['JERRY', 'Do you know what this is all about?\
         Do you know, why were here? To be out, \
        this is out...and out is one of the single most enjoyable \
            experiences of life. People...\
        did you ever hear people talking about We should go out?\
        This is what theyre talking about...\
        this whole thing, were all out now, no one is home. Not one \
        person here is home, were all out! \
        There are people tryin to find us, they dont know \
        where we are. (on an imaginary phone) Did you ring?, \
        I cant find him. Where did he go? He didnt tell me where he was going. \
        He must have gone out. You wanna go out you get ready, \
        you pick out the clothes, right? You take \
        the shower, you get all ready, get the cash, \
        get your friends, the car, the spot, the reservation..\
        .Then youre standing around, whatta you do? You go \
        We gotta be getting back. Once youre out, \
        you wanna get back! You wanna go to sleep, you wanna get up, \
        you wanna go out again tomorrow, right? \
        Where ever you are in life, its my feeling, youve gotta go.',
         'S01E01',
         1, 1, 0.24, 0, 0, 0.41, 0.35, 189],
        ['JERRY', '(pointing at Georges shirt) See, to me, that button is in \
        the worst possible spot. \
        The second button literally makes or breaks the shirt, look at it.\
        Its too high! Its in no-mans-land. \
        You look like you live with your mother.',
         'S01E01', 1, 1, 0, 0, 0.33, 0.33, 0.33, 41],
        ['GEORGE', 'Are you through?', 'S01E01', 1, 1, 0, 0, 0, 0, 0, 3],
        ['JERRY', 'You do of course try on, when you buy?',
            'S01E02', 1, 1, 0, 0, 0, 0, 0, 9],
        ['GEORGE', 'Yes, it was purple, I liked it, I dont actually recall \
        considering the buttons.', 'S01E02', 1, 2, 0, 0.5, 0, 0.5, 0, 14],
    ]

    mock_imdb_data = pd.DataFrame(
        data_imdb_raw, columns=['Season',
                                'EpisodeNo', 'AirDate', 'Writers',
                                'Director', 'SEID', 'tconst',
                                'Title', 'EpiNo_Netflix', 'runtimeMinutes',
                                'numVotes', 'averageRating',
                                'Description', 'Summaries', 'keyWords'])
    mock_script_data = pd.DataFrame(data_scripts_raw, columns=[
        'Character', 'Dialogue', 'SEID', 'Season', 'EpisodeNo',
        'Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'numWords'])

    if args[0] == data_constants.SCRIPTS_LINK:
        return mock_script_data
    return mock_imdb_data
