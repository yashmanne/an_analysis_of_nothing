![](./an_analysis_of_nothing/static/images/analysis_of_nothing.png)

---
[![Coverage Status](https://coveralls.io/repos/github/yashmanne/an_analysis_of_nothing/badge.svg)](https://coveralls.io/github/yashmanne/an_analysis_of_nothing)

<a id="tntroduction"></a>
## Introduction
The '90s hit, ***Seinfeld***, is an American sitcom that features four friends, Jerry Seinfeld (Jerry Seinfeld), George Costanza (Jason Alexander), Elaine Benes (Julia Louis-Dreyfus), and Cosmo Kramer (Michael Richards), and their daily lives in New York City. The show follows Jerry, a stand-up comedian, and the lives of his best friend, George, his neighbor, Kramer, and his ex-girlfriend, Elaine, all played by real-life comedians. The show has been characterized as a “show about nothing”. While its popularity peaked in the '90s, the show continues to garner new fans while retaining old ones. It is recognized as one of the most influential sitcoms in TV history.  

Despite the show having cemented its place as one of the greatest sitcoms to date, it can be difficult for *Seinfeld* fans, as well as those curious about the show, to search and discover certain episode and series characteristics when their only resource is manual web-searching. To this, we develop an interactive web application that covers the extensive capabilities of Wikipedia, IMDb, and Netflix all in one–acting as a descriptive and exploratory tool for users to query specific scenes, visualize character quirks, and receive recommendations for future watches. We hope to not only uncover new insights about the classic show, but also provide a centralized **tool** for fans to access and explore all things *Seinfeld*!

Public Website: **[nothing.streamlit.app](https://nothing.streamlit.app/)**


#### Team Members:
| Name | GitHub | Name | GitHub |
|:------:|:------:|:------:|:------:|
| **Yash Manne** | *yashmanne*| **Yamina Katariya** | *YaminaKat7* |
| **Aditi Shrivastava** | *ad-iti* | **Chandler Ault** | *Dreamweaver2k* |

## Table of Contents
* [Introduction](#introduction)
* [Tasks of Interest](#tasks-of-interest)
* [Repository Structure](#repository-structure)
* [Installation](#installation)
  * [Environment](#environment)
  * [Data](#data)
  * [Application](#application)
* [Examples](#examples)

<a id="tasks-of-interest"></a>
## Tasks of Interest
- **Interactive Visual Homepage**:
  - Chronicles number of dialogue lines for each character across the series across an interactive visual dashboard.
  - Showcases change in episode rating across the series.
- **Search Query**:
  - Allows users to search for specific episodes based on partially remembered dialogue snippets or keywords.
  - Includes additional ***advanced search*** functionality for filtering search based on season, episode rating, and desired characters.
  - Showcases multiple visualizations detailing the emotional distribution of the episode among the main characters.
- **Episode Recommender**:
  - Finds similar episode(s) to a user's favorite(s) based on dialogue, episode description, IMDb keywords, episode summary, emotional distribution of each character, the number of lines for each character, and the IMDb audience rating.
  
<a id="repository-structure"></a>
## Repository Structure
NEED TO UPDATE AFTER EXAMPLES ARE DONE.
```
├── an_analysis_of_nothing/
│   ├── app_pages/
│   │   ├── __init__.py
│   │   ├── write_about_page.py
│   │   ├── write_episode_query.py
│   │   ├── write_home_page.py
│   │   ├── write_recommender_page.py
│   ├── static/
│   │   ├── data/
│   │   │   ├── dialogue_tensors/
│   │   │   │   ├── tensor_0.npy
│   │   │   │   ├── tensor_1.npy
│   │   │   │   ├── ...
│   │   │   │   ├── tensor_9.npy
│   │   │   ├── metadata.csv
│   │   │   ├── scripts.csv
│   │   │   ├── README.md
│   │   ├── images/
│   │   │   ├── analysis_of_nothing.png
│   │   │   ├── elaine.png
│   │   │   ├── elaine_.jpg
│   │   │   ├── elaine_typing.gif
│   │   │   ├── george.png
│   │   │   ├── george_.jpg
│   │   │   ├── giphy.gif
│   │   │   ├── jerry.png
│   │   │   ├── kramer.png
│   │   │   ├── kramer_.jpg
│   │   │   ├── lead.png
│   │   │   ├── newman_.jpg
│   │   │   ├── README.md
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── mock_functions.py
│   │   ├── test_data_manager.py
│   │   ├── test_episode_query.py
│   │   ├── test_recommender.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_constants.py
│   │   ├── data_manager.py
│   │   ├── episode_query.py
│   │   ├── recommender.py
│   ├── app.py
│   ├── README.md
│   ├── requirements.txt
├── doc/
│   ├── Component_Specification.md
│   ├── Episode_Query_Interaction.png
│   ├── Episode_Recommender_Interaction.png
│   ├── Functional_Specification.md
│   ├── General_Analytics_Interaction.png
│   ├── README.md
│   ├── Sequence_Diagram.png
│   ├── Technology Review.pptx          ## Rename and change to PDF
├── examples/
│   ├── README.md
├── scripts/
│   ├── data_tools/
│   │   ├── __init__.py
│   │   ├── _scrape_epi_pages.py
│   │   ├── data_constants.py
│   │   ├── load_data.py
│   ├── precompute_tools/
│   │   ├── __init__.py 
│   │   ├── query_vectors.py
│   │   ├── sentiment.py
│   ├── get_final_data.py
│   ├── README.md
├── .gitignore
├── environment.yml
├── .gitignore
├── LICENSE
├── pylintrc
├── pyproject.toml
├── README.md (Current File)
```

<a id="installation"></a>
## Installation

This repository can be cloned locally by running the following `git` command:
```bash
git clone https://github.com/yashmanne/an_analysis_of_nothing.git
```
Please note that Git is required to run the above command. For instructions on downloading Git, please see [the GitHub guide](https://github.com/git-guides/install-git).

<a id="environment"></a>
### Environment
This application is built on top of multiple Python packages with specific version requirements. Installing these packages can cause conflicts with other packages in the workspace. As a work-around, we recommend to use `conda` to create an isolated Python environment with all necessary packages. Specifically, the list of necessary packages can be found at in the [`environment.yml`](./environment.yml) file.

To create our specified `nothing` Conda environment, run the following command:
```bash
conda create -f environment.yml
```

Once the Conda environment is created, it can be activated by:
```bash
conda activate nothing
```
After coding inside the environment, it can be deactivated with the command:
```bash
conda deactivate
```

Please note that Conda must be installed for the above commands to work. For instructions on installing Conda, please visit [Conda.io](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

<a id="data"></a>
### Data
The raw data for our project was obtained from three different sources:
1. Complete script dialogue and metadata for all episodes was found on [Kaggle](https://www.kaggle.com/thec03u5/seinfeld-chronicles).
2. Additional production information and audience rating was obtained from [IMDb](https://www.imdb.com/interfaces/).
3. Individual IMDb episode pages were scraped for additional information such as episode summary, episode description, and episode keywords.

To process & store the data for future analyses, run the following code:
```bash
conda activate nothing
python ./scripts/get_final_data.py
conda deactivate
```
Please note that this code not only cleans & merges the data, but also calculates the emotional distribution of each dialogue line and generates a pretrained BERT vector embedding for each line. This script may take up to 3 hours.

More details can be found \[ here \] \(). @ADITI

<a id="application"></a>
### Application
We generated our application through the open-source `streamlit` package. A local application can be generated with the code:
```bash
conda activate nothing
streamlit run an_analysis_of_nothing/app.py
```
This will pop up a browser window with the functioning web-application.
More details can be found \[HERE\]\(\) @ ADITI.

<a id="examples"></a>
## Examples
A demonstration of our working application can be seen [here](https://github.com/HWNi/DATA515-Project/blob/master/examples/EXAMPLES.md).

More details on how to run our code can be found [here](./examples/README.md).
