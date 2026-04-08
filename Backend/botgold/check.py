import pandas as pd

DOWNLOAD_PATH = "./data"

# datasets = {
#     "GDP": "pib_per_capita_countries_dataset.csv",
#     "Inflation": "global_inflation_countries.csv",
#     "Gold": "Gold Price Prediction.csv",
#     "XAU": "XAU_1d_data.csv",
# }

datasets = {
    "GDP": "new_pib_per_capita_countries_dataset.csv",
    "Inflation": "new_global_inflation_countries.csv",
    "Gold": "new_gold_price_prediction.csv",
    "XAU": "new_xau_1d_data.csv",
}

for name, file in datasets.items():
    sep = ";" if file == "XAU_1d_data.csv" else ","
    df = pd.read_csv(f"{DOWNLOAD_PATH}/{file}", sep=sep)
    
    print(f"\n{'='*40}")
    print(f"[{name}] shape: {df.shape}")
    print(f"columns: {df.columns.tolist()}")
    
    missing = pd.DataFrame({
        'missing_count': df.isnull().sum(),
        'missing_percent': (df.isnull().sum() / len(df) * 100).round(2)
    })
    missing = missing[missing['missing_count'] > 0].sort_values('missing_percent', ascending=False)
    
    if missing.empty:
        print("missing: ไม่มี")
    else:
        print(f"missing:\n{missing}")