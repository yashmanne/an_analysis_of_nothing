# Examples

## Deployment
Our app was deployed using Streamlit Sharing via https://share.streamlit.io/. 
Learn more about [deploying](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app) and [sharing](https://docs.streamlit.io/streamlit-community-cloud/get-started/share-your-app#sharing-public-apps) a public Streamlit web app.

Public Website: [nothing.streamlit.app](https://nothing.streamlit.app/)
Navigate to the GitHub icon in the top right to view source material.

## Running Locally

### 1. Clone the Git Repo

Run the following `git` command:
```bash
git clone https://github.com/yashmanne/an_analysis_of_nothing.git
```

### 2. Local Environment Setup

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

### 3. Loading Data 

To process & store the data for future analyses, run the following code:
```bash
conda activate nothing
python ./scripts/get_final_data.py
conda deactivate
```

Click [here](data.ipynb) for further examples on how our data is stored, preprocessed, and used.

### 4. Run the app

A local application can be generated with the code:
```bash
conda activate nothing
streamlit run an_analysis_of_nothing/app.py
```

See An Analysis of Nothing in your local browser!


## Navigating the site

Click [here](site_examples.ipynb) for a website walkthrough.
