import pandas as pd
from download import DOWNLOAD_PATH

def convert_xau():
    df = pd.read_csv(f"{DOWNLOAD_PATH}/new_xau_1d_data.csv")
    
    documents = []
    for _, row in df.iterrows():
        # ข้อมูลจริงมี: Date, Open, High, Low, Close, Volume
        text = (
            f"On {row['Date']}, gold (XAU/USD): "
            f"Open was {row['Open']} USD, "
            f"High was {row['High']} USD, "
            f"Low was {row['Low']} USD, "
            f"Close was {row['Close']} USD, "
            f"Volume was {row['Volume']}."
        )
        documents.append(text)
    
    return documents

if __name__ == "__main__":
    docs = convert_xau()
    print(f"Total documents: {len(docs)}")
    print("Example:")
    print(docs[0])