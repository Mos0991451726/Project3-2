import pandas as pd
from download import DOWNLOAD_PATH

def clean_gdp():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/pib_per_capita_countries_dataset.csv")
    
    # ลบ meta cols
    drop_cols = [
        'region','intermediate_region'
    ]
    new_df = df.drop(columns=drop_cols)
    
    # แปลง year
    new_df['year'] = pd.to_datetime(new_df['year'], format='%Y')
    
    # drop แถวที่ missing
    new_df = new_df.dropna(subset=['gdp_variation'])
    
    new_df.to_csv(f"{DOWNLOAD_PATH}/new_pib_per_capita_countries_dataset.csv", index=False)
    print(f"GDP cleaned! shape: {new_df.shape}")
    return new_df

if __name__ == "__main__":
    clean_gdp()