"""
Contains functions to apply sentiment analysis to data.
"""
import pandas as pd
import text2emotion as te
from tqdm.auto import tqdm


def get_emotions(scripts):
    """
    Get emotion probabilities for each dialogue in data.
    NOTE: This takes a long time to run.( >2 Hrs)
    :param: scripts: Pandas DataFrame containing at least these columns:
                 'Character', 'Dialogue', 'SEID' representing the script data.
                 RAISE VALUE ERROR ELSE
    :return: data frame with additional columns for each of the emotions:
            'Happy', 'Angry', 'Surprise', 'Sad', 'Fear'
    """
    tqdm.pandas()
    scripts['Emotion'] = scripts.Dialogue.progress_apply(te.get_emotion)
    emotions = pd.json_normalize(scripts['Emotion'])
    for col in emotions.columns:
        scripts[col] = emotions[col]
    scripts['numWords'] = scripts.Dialogue.apply(lambda x: len(x.split()))
    scripts.drop(columns=['Emotion'], inplace=True)
    return scripts
