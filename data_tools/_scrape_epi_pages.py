"""
Contains functions to scrape addititional information from each
episode's IMDb page. Specifically, the code will extract:
    * Episode Descriptions
    * Episode Summaries
    * Episode Keywords
This script is run to generate scraped information that is stored
as `data_constants.Summaries` on Google Drive
"""
import pandas as pd
from tqdm.auto import tqdm

from bs4 import BeautifulSoup
import requests

from . import data_constants

def scrape_data():
    """
    This function scrapes episode descriptions, user-generated plot
    summaries, and user-generated plot keywords from the IMDb pages
    of each episoode.

    :return: Pandas Data Frame
    """
    seinfeld_id = data_constants.SEINFELD_PARENT_TCONST
    # Gather all episode metadata
    print('Gathering Episode Info...')
    all_eps = pd.read_csv(data_constants.IMDB_EPISODE, delimiter='\t')
    all_eps = all_eps[all_eps.parentTconst == seinfeld_id]
    #   Season 5, Episode 19 doubled in data.
    epi_ids = set(all_eps['tconst'].values) - {'tt19390512'}
    # Gather all episode summary and keyword data
    print('Gathering Episode Descriptions, Summaries, and Keywords...')
    texts = {
        epi_id: {
            'Description': '',
            'Summaries': [],
            'keyWords': []
        }
        for epi_id in epi_ids
    }
    # IMDb Description From Season Pages
    for szn in tqdm(range(1, 10), desc="Scraping IMDb Descriptions"):
        url = data_constants.IMDB_DESC.format(szn=szn)
        response = requests.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
        episodes = page.find_all('div', class_='info')
        for episode in tqdm(episodes, leave=False):
            epi_id = str(episode.find('strong')).split('title/')[1]
            epi_id = epi_id.split('/')[0]
            description = episode.find('div',
                class_='item_description').text.strip()
            if epi_id in epi_ids:
                texts[epi_id]['Description'] = description
            # Append decription of part II of the Raincoats (S5E18-19)
            # Summaries & keywords don't need to be updated
            elif epi_id == 'tt19390512':
                updated_desc = texts['tt0697764']['Description'] +\
                    '\n' + description
                texts['tt0697764']['Description'] = updated_desc
    # Parse Individual Episode Pages
    for epi_id in tqdm(epi_ids, desc="Scraping Summaries & Key Words"):
        # User Summaries
        url = data_constants.IMDB_SUMMARY.format(tconst=epi_id)
        response = requests.get(url, headers=data_constants.HDR)
        page = BeautifulSoup(response.text, 'html.parser')
        summaries = [summary.get_text()
            for summary in page.find_all('div',
                class_="ipc-html-content-inner-div")]
        for summary in summaries:
            if summary not in texts[epi_id]['Summaries']:
                texts[epi_id]['Summaries'].append(summary)
        # IMDb Key Words
        url = data_constants.IMDB_KWORDS.format(tconst=epi_id)
        response = requests.get(url, headers=data_constants.HDR)
        page = BeautifulSoup(response.text, 'html.parser')
        keywords = [kw.get_text().split('\n')[1]
            for kw in page.find_all('div', class_="sodatext")]
        for keyword in keywords:
            texts[epi_id]['keyWords'].append(keyword)

    texts = pd.DataFrame(texts).T.reset_index()
    texts['Summaries'] = texts.Summaries.apply(lambda x: x[1:])
    texts = texts.rename(columns={'index': 'tconst'})

    # Clean up summaries to remove author tags:
    remove_author_tag = lambda summaries: \
        [summary.split('—')[0] if len(summary.split('—')) == 2
            else summary for summary in summaries]
    texts.Summaries = texts.Summaries.apply(remove_author_tag)
    return texts

if __name__ == '__main__':
    scrape_data()
