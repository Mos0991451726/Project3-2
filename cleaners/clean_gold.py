import pandas as pd
from download import DOWNLOAD_PATH

def clean_gold():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/Gold Price Prediction.csv")
    
    # แปลง Date
    new_df = df.copy()
    new_df['Date'] = pd.to_datetime(new_df['Date'], format='%m/%d/%y')
    
    # drop แถวที่ missing
    new_df = new_df.dropna(subset=[
        'Price Change Ten',
        'Std Dev 10',
        'Price Change Tomorrow',
        'Price Tomorrow'
    ])
    
    new_df.to_csv(f"{DOWNLOAD_PATH}/new_gold_price_prediction.csv", index=False)
    print(f"Gold cleaned! shape: {new_df.shape}")
    return new_df

if __name__ == "__main__":
    clean_gold()