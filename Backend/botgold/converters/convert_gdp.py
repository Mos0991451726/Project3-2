 
import pandas as pd
from download import DOWNLOAD_PATH

def convert_gdp():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/new_pib_per_capita_countries_dataset.csv")
    
    documents = []
    for _, row in df.iterrows():
        # ข้อมูลจริงมี: country_code, country_name, sub_region, indicator_code, indicator_name, year, gdp_per_capita, gdp_variation
        text = (
            f"In {row['year'][:4]}, {row['country_name']} ({row['sub_region']}) "
            f"had a GDP per capita of {row['gdp_per_capita']:,.2f} USD, "
            f"with a GDP variation of {row['gdp_variation']}%."
        )
        documents.append(text)
    
    return documents

if __name__ == "__main__":
    docs = convert_gdp()
    print(f"Total documents: {len(docs)}")
    print("Example:")
    print(docs[0])