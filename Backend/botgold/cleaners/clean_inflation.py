import pandas as pd
from download import DOWNLOAD_PATH

def clean_inflation():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/global_inflation_countries.csv")
    
    # ลบ meta cols
    drop_cols = [
        'region','intermediate_region'
    ]
    new_df = df.drop(columns=drop_cols)
    
    # แปลง year
    new_df['year'] = pd.to_datetime(new_df['year'], format='%Y')
    
    new_df.to_csv(f"{DOWNLOAD_PATH}/new_global_inflation_countries.csv", index=False)
    print(f"Inflation cleaned! shape: {new_df.shape}")
    return new_df

if __name__ == "__main__":
    clean_inflation()