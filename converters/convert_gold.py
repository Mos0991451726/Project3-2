import pandas as pd
from download import DOWNLOAD_PATH

def convert_gold():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/new_gold_price_prediction.csv")
    
    documents = []
    for _, row in df.iterrows():
        text = (
            f"On {row['Date']}, gold market data: "
            f"Price Today was {row['Price Today']} USD, "
            f"Price Tomorrow was {row['Price Tomorrow']} USD, "
            f"Monthly Inflation Rate was {row['Monthly Inflation Rate']}%, "
            f"EFFR Rate was {row['EFFR Rate']}%, "
            f"Treasury Par Yield Month was {row['Treasury Par Yield Month']}%, "
            f"Treasury Par Yield Two Year was {row['Treasury Par Yield Two Year']}%, "
            f"Treasury Par Yield 10 Year was {row['Treasury Par Yield Curve Rates (10 Yr)']}%, "
            f"DXY was {row['DXY']}, SP Open was {row['SP Open']}, "
            f"VIX was {row['VIX']}, Crude Oil was {row['Crude']} USD."
        )
        documents.append(text)
    return documents

if __name__ == "__main__":
    docs = convert_gold()
    print(f"Total documents: {len(docs)}")
    print("Example:")
    print(docs[0])