import pandas as pd
from download import DOWNLOAD_PATH

def clean_xau():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/XAU_1d_data.csv", sep=";")
    
    new_df = df.copy()
    
    # แปลง Date
    new_df['Date'] = pd.to_datetime(new_df['Date'], format='%Y.%m.%d %H:%M')
    new_df['Date'] = new_df['Date'].dt.date
    
    new_df.to_csv(f"{DOWNLOAD_PATH}/new_xau_1d_data.csv", index=False)
    print(f"XAU cleaned! shape: {new_df.shape}")
    return new_df

if __name__ == "__main__":
    clean_xau()