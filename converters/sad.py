import pandas as pd
from downloader import DOWNLOAD_PATH

def convert_analysis():
    documents = []
    
    # === XAU: ราคาสูงสุด/ต่ำสุดแต่ละปี + % เปลี่ยนแปลง ===
    xau = pd.read_csv(f"{DOWNLOAD_PATH}/new_xau_1d_data.csv")
    xau['Date'] = pd.to_datetime(xau['Date'])
    xau['year'] = xau['Date'].dt.year
    
    for year, group in xau.groupby('year'):
        high = group['High'].max()
        low = group['Low'].min()
        start = group.iloc[-1]['Close']
        end = group.iloc[0]['Close']
        change = ((end - start) / start * 100).round(2)
        
        text = (
            f"ในปี {year} ราคาทองคำ (XAU/USD) สูงสุดอยู่ที่ {high} ดอลลาร์ "
            f"ต่ำสุดอยู่ที่ {low} ดอลลาร์ "
            f"และราคาเปลี่ยนแปลงตลอดปี {change}%"
        )
        documents.append(text)
    
    # === Gold: ความสัมพันธ์ DXY, VIX, EFFR กับราคาทอง ===
    gold = pd.read_csv(f"{DOWNLOAD_PATH}/new_gold_price_prediction.csv")
    
    for _, row in gold.iterrows():
        text = (
            f"เมื่อวันที่ {row['Date']} ค่าดอลลาร์ (DXY) อยู่ที่ {row['DXY']} "
            f"ความกลัวตลาด (VIX) อยู่ที่ {row['VIX']} "
            f"อัตราดอกเบี้ย (EFFR) อยู่ที่ {row['EFFR Rate']}% "
            f"ราคาน้ำมัน (Crude) อยู่ที่ {row['Crude']} ดอลลาร์ "
            f"ราคาทองวันนั้นอยู่ที่ {row['Price Today']} ดอลลาร์"
        )
        documents.append(text)
    
    # === GDP + Inflation: เปรียบเทียบ ===
    gdp = pd.read_csv(f"{DOWNLOAD_PATH}/new_pib_per_capita_countries_dataset.csv")
    inflation = pd.read_csv(f"{DOWNLOAD_PATH}/new_global_inflation_countries.csv")
    
    merged = pd.merge(gdp, inflation, on=['country_name', 'year'], how='inner')
    
    for _, row in merged.iterrows():
        text = (
            f"ในปี {row['year'][:4]} ประเทศ {row['country_name']} "
            f"มี GDP per capita {row['gdp_per_capita']:,.2f} ดอลลาร์ "
            f"อัตราเงินเฟ้อ {row['inflation_rate']}% "
            f"ประเทศที่มีเงินเฟ้อสูงมักหันมาถือทองคำเพื่อรักษามูลค่า"
        )
        documents.append(text)
    
    print(f"Analysis documents: {len(documents)}")
    return documents

if __name__ == "__main__":
    docs = convert_analysis()
    print(f"Total: {len(docs)}")
    print("Example:")
    print(docs[0])  