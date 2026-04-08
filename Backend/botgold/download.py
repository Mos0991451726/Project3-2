import os
from kaggle.api.kaggle_api_extended import KaggleApi

DOWNLOAD_PATH = "./data"

DATASETS = [
    {
        "dataset": "fredericksalazar/global-gdp-pib-per-capita-dataset-1960-present",
        "check_file": "pib_per_capita_countries_dataset.csv"
    },
    {
        "dataset": "fredericksalazar/global-inflation-rate-1960-present",
        "check_file": "global_inflation_countries.csv"
    },
    {
        "dataset": "cvergnolle/gold-price-and-relevant-metrics",
        "check_file": "Gold Price Prediction.csv"
    },
    {
        "dataset": "novandraanugrah/xauusd-gold-price-historical-data-2004-2024",
        "check_file": "XAU_1d_data.csv"
    },
]

def download_all():
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    
    api = KaggleApi()
    api.authenticate()

    for item in DATASETS:
        filepath = os.path.join(DOWNLOAD_PATH, item["check_file"])
        if os.path.exists(filepath):
            print(f"Already exists, skipping: {item['check_file']}")
            continue
        
        print(f"Downloading {item['dataset']}...")
        api.dataset_download_files(item["dataset"], path=DOWNLOAD_PATH, unzip=True)
        print(f"Done!")

if __name__ == "__main__":
    download_all()