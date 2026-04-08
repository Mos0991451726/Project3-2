import pandas as pd
from download import DOWNLOAD_PATH

def convert_inflation():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/new_global_inflation_countries.csv")
    
    documents = []
    for _, row in df.iterrows():
        # ข้อมูลจริงมี: country_code, country_name, sub_region, indicator_code, indicator_name, year, inflation_rate
        text = (
            f"In {row['year'][:4]}, {row['country_name']} ({row['sub_region']}) "
            f"had an inflation rate of {row['inflation_rate']}%."
        )
        documents.append(text)
    
    return documents

if __name__ == "__main__":
    docs = convert_inflation()
    print(f"Total documents: {len(docs)}")
    print("Example:")
    print(docs[0])